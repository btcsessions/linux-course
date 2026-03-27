"""Rich-based lesson renderer with pagination."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from cachycli.core.lesson_loader import Lesson
from cachycli.ui.theme import CACHYCLI_THEME, LESSON_BORDER


def render_lesson(lesson: Lesson, console: Console | None = None) -> None:
    """Display a lesson in the terminal with styled Rich output."""
    con = console or Console(theme=CACHYCLI_THEME)
    width = min(con.width, 90)

    # Header
    header = Text()
    header.append(f"Lesson {lesson.id}", style="title")
    header.append(f"  |  Week {lesson.week}", style="info")
    header.append(f"  |  ~{lesson.duration_minutes} min", style="muted")
    con.print()
    con.print(
        Panel(
            header,
            title=f"[title]{lesson.title}[/title]",
            border_style=LESSON_BORDER,
            width=width,
        )
    )

    # Learning objectives
    obj_lines = Text()
    for i, obj in enumerate(lesson.objectives, 1):
        obj_lines.append(f"  {i}. ", style="muted")
        obj_lines.append(obj, style="objective")
        obj_lines.append("\n")
    con.print(
        Panel(
            obj_lines,
            title="[heading]Learning Objectives[/heading]",
            border_style=LESSON_BORDER,
            width=width,
        )
    )

    # Key commands
    if lesson.commands:
        cmds = "  ".join(f"[command]{c}[/command]" for c in lesson.commands)
        con.print(
            Panel(
                cmds,
                title="[heading]Key Commands[/heading]",
                border_style=LESSON_BORDER,
                width=width,
            )
        )

    # Lesson body (markdown)
    con.print()
    md = Markdown(lesson.body, code_theme="monokai")

    # Paginate: split and display in chunks
    _paginated_print(con, md, width)

    con.print()
    con.print("[success]--- End of Lesson ---[/success]", justify="center")
    con.print()


def _paginated_print(
    con: Console, renderable: object, width: int, page_lines: int = 30
) -> None:
    """Print renderable content with pagination (press Enter to continue)."""
    with con.capture() as capture:
        con.print(renderable, width=width)
    output = capture.get()
    lines = output.split("\n")

    for i in range(0, len(lines), page_lines):
        chunk = "\n".join(lines[i : i + page_lines])
        con.print(chunk, highlight=False)
        if i + page_lines < len(lines):
            con.print("[muted]--- Press Enter to continue ---[/muted]", justify="center")
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                return
