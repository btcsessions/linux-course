"""Progress dashboard rendered with Rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cachycli.core.progress import ProgressDB
from cachycli.core.scheduler import LESSONS_PER_WEEK, TOTAL_LESSONS, week_progress
from cachycli.ui.theme import CACHYCLI_THEME, PROGRESS_BORDER

_WEEK_NAMES = [
    "Terminal & Navigation",
    "File Operations",
    "Viewing & Editing",
    "Permissions & Users",
    "Text Processing",
    "Pipes & Redirection",
    "System Admin (CachyOS)",
]

_TOTAL_WEEKS = 7


def render_progress(db: ProgressDB, console: Console | None = None) -> None:
    con = console or Console(theme=CACHYCLI_THEME)
    width = min(con.width, 80)

    current_streak, longest_streak = db.get_streak()
    completed = db.completed_count()

    # Summary header
    summary = Text()
    summary.append("  Current Streak: ", style="muted")
    summary.append(f"{current_streak} days", style="streak")
    summary.append("    Longest: ", style="muted")
    summary.append(f"{longest_streak} days\n", style="streak")
    summary.append(f"  Lessons Completed: ", style="muted")
    summary.append(f"{completed}/{TOTAL_LESSONS}\n", style="subtitle")

    # Average quiz score
    results = db.all_quiz_results()
    if results:
        avg = sum(r.percentage for r in results) / len(results)
        summary.append(f"  Average Quiz Score: ", style="muted")
        summary.append(f"{avg:.0f}%\n", style="subtitle")

    con.print()
    con.print(
        Panel(
            summary,
            title="[title]CachyCLI Progress[/title]",
            border_style=PROGRESS_BORDER,
            width=width,
        )
    )

    # Per-week table
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        width=width,
    )
    table.add_column("Week", style="bold", width=6)
    table.add_column("Topic", width=26)
    table.add_column("Progress", width=22)
    table.add_column("Quiz", width=14)

    for week in range(1, _TOTAL_WEEKS + 1):
        done, total = week_progress(db, week)
        bar_filled = int(done / total * 10)
        bar = "[cyan]" + "#" * bar_filled + "[/cyan]" + "[dim]." * (10 - bar_filled) + "[/dim]"
        progress_str = f"{bar} {done}/{total}"

        quiz_result = db.best_quiz_result("weekly", f"week_{week:02d}")
        if quiz_result:
            if quiz_result.percentage >= 70:
                quiz_str = f"[green]{quiz_result.percentage:.0f}% PASS[/green]"
            else:
                quiz_str = f"[red]{quiz_result.percentage:.0f}%[/red]"
        elif done == total:
            quiz_str = "[yellow]Ready[/yellow]"
        else:
            quiz_str = "[dim]--[/dim]"

        name = _WEEK_NAMES[week - 1] if week <= len(_WEEK_NAMES) else f"Week {week}"
        table.add_row(str(week), name, progress_str, quiz_str)

    con.print(table)
    con.print()
