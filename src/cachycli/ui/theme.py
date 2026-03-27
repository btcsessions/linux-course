"""Consistent color palette and styling tokens for the CachyCLI TUI."""

from rich.theme import Theme

CACHYCLI_THEME = Theme(
    {
        "title": "bold cyan",
        "subtitle": "bold white",
        "heading": "bold bright_cyan",
        "objective": "green",
        "command": "bold yellow",
        "success": "bold green",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "dim cyan",
        "muted": "dim white",
        "streak": "bold bright_yellow",
        "progress.bar": "cyan",
        "quiz.correct": "bold green",
        "quiz.wrong": "bold red",
        "quiz.explanation": "italic dim white",
        "prompt": "bold bright_white",
    }
)

# Box styles
PANEL_BORDER = "cyan"
LESSON_BORDER = "bright_cyan"
QUIZ_BORDER = "bright_green"
PROGRESS_BORDER = "bright_yellow"
