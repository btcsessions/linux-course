"""Textual-based interactive quiz view."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Footer, Header, Label, Static

from cachycli.core.quiz_engine import Question, Quiz, check_answer


class QuizComplete(Exception):
    """Raised when the quiz is finished -- carries score info."""

    def __init__(self, score: int, total: int) -> None:
        self.score = score
        self.total = total


class QuestionWidget(Static):
    """Displays a single question and collects the answer."""

    def __init__(self, question: Question, number: int, total: int) -> None:
        super().__init__()
        self.question = question
        self.number = number
        self.total = total

    def compose(self) -> ComposeResult:
        q = self.question
        yield Label(
            f"[bold cyan]Question {self.number}/{self.total}[/bold cyan]",
            id="q-header",
        )
        yield Label(f"\n{q.question}\n", id="q-text")

        if q.type == "multiple_choice":
            for i, choice in enumerate(q.choices):
                yield Label(f"  [yellow]{i}[/yellow]) {choice}")
            yield Label("\n[dim]Type the number of your answer and press Enter.[/dim]")
        elif q.type == "true_false":
            yield Label("  [yellow]t[/yellow]) True")
            yield Label("  [yellow]f[/yellow]) False")
            yield Label("\n[dim]Type t or f and press Enter.[/dim]")
        elif q.type == "fill_in_blank":
            yield Label("\n[dim]Type your answer and press Enter.[/dim]")


class QuizApp(App[tuple[int, int]]):
    """Interactive quiz application using Textual."""

    CSS = """
    Screen {
        background: $surface;
    }
    #quiz-container {
        padding: 1 2;
    }
    #q-header {
        color: cyan;
        text-style: bold;
    }
    #feedback {
        margin-top: 1;
        padding: 1 2;
    }
    #input-label {
        margin-top: 1;
    }
    #score-summary {
        margin: 2 0;
        padding: 1 2;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit_quiz", "Quit", show=True),
    ]

    def __init__(self, quiz: Quiz) -> None:
        super().__init__()
        self.quiz = quiz
        self.current_index = 0
        self.score = 0
        self.total = len(quiz.questions)
        self.waiting_for_answer = True
        self.answer_buffer = ""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="quiz-container"):
            title = "Weekly Quiz" if self.quiz.quiz_type == "weekly" else "Lesson Quiz"
            yield Label(f"[bold bright_cyan]{title}: {self.quiz.quiz_id}[/bold bright_cyan]\n")
            yield Container(id="question-area")
        yield Footer()

    def on_mount(self) -> None:
        self._show_question()

    def _show_question(self) -> None:
        area = self.query_one("#question-area")
        area.remove_children()
        if self.current_index >= self.total:
            self._show_results(area)
            return
        q = self.quiz.questions[self.current_index]
        area.mount(QuestionWidget(q, self.current_index + 1, self.total))
        area.mount(Label("", id="input-label"))
        area.mount(Label("", id="feedback"))
        self.waiting_for_answer = True
        self.answer_buffer = ""
        self._update_input_display()

    def _update_input_display(self) -> None:
        try:
            lbl = self.query_one("#input-label", Label)
            lbl.update(f"[bold bright_white]> {self.answer_buffer}_[/bold bright_white]")
        except Exception:
            pass

    def on_key(self, event) -> None:
        if not self.waiting_for_answer:
            # Any key after feedback moves to next question.
            self.current_index += 1
            self._show_question()
            return

        if event.key == "enter":
            self._submit_answer()
        elif event.key == "backspace":
            self.answer_buffer = self.answer_buffer[:-1]
            self._update_input_display()
        elif event.is_printable and event.character:
            self.answer_buffer += event.character
            self._update_input_display()

    def _submit_answer(self) -> None:
        if not self.answer_buffer.strip():
            return
        q = self.quiz.questions[self.current_index]
        correct = check_answer(q, self.answer_buffer.strip())
        if correct:
            self.score += 1

        feedback = self.query_one("#feedback", Label)
        if correct:
            msg = "[bold green]Correct![/bold green]"
        else:
            if q.type == "multiple_choice":
                right = q.choices[q.answer] if isinstance(q.answer, int) else q.answer
            elif q.type == "true_false":
                right = "True" if q.answer else "False"
            else:
                right = str(q.answer)
            msg = f"[bold red]Incorrect.[/bold red] The answer is: [yellow]{right}[/yellow]"

        if q.explanation:
            msg += f"\n[italic dim]{q.explanation}[/italic dim]"
        msg += "\n\n[dim]Press any key to continue...[/dim]"
        feedback.update(msg)
        self.waiting_for_answer = False

    def _show_results(self, area: Container) -> None:
        pct = (self.score / self.total * 100) if self.total else 0
        passed = pct >= 70
        status = "[bold green]PASSED[/bold green]" if passed else "[bold red]NOT PASSED[/bold red]"
        area.mount(
            Label(
                f"\n[bold bright_cyan]Quiz Complete![/bold bright_cyan]\n\n"
                f"Score: [bold]{self.score}/{self.total}[/bold] ({pct:.0f}%)\n"
                f"Status: {status}\n\n"
                f"[dim]Press any key to exit...[/dim]",
                id="score-summary",
            )
        )
        self.waiting_for_answer = False

    def action_quit_quiz(self) -> None:
        self.exit((self.score, self.total))

    def on_key_after_results(self, event) -> None:
        if self.current_index >= self.total:
            self.exit((self.score, self.total))


def run_quiz(quiz: Quiz) -> tuple[int, int]:
    """Run the quiz TUI and return (score, total)."""
    app = QuizApp(quiz)
    result = app.run()
    if isinstance(result, tuple):
        return result
    return app.score, app.total
