"""Click CLI entry point for CachyCLI."""

from __future__ import annotations

import click
from rich.console import Console

from cachycli import __version__
from cachycli.core.lesson_loader import load_all_lessons, load_lesson
from cachycli.core.progress import ProgressDB
from cachycli.core.quiz_engine import load_lesson_quiz, load_weekly_quiz
from cachycli.core.scheduler import (
    TOTAL_LESSONS,
    current_week,
    is_week_complete,
    next_lesson_id,
    week_progress,
)
from cachycli.ui.lesson_view import render_lesson
from cachycli.ui.progress_view import render_progress
from cachycli.ui.quiz_view import run_quiz
from cachycli.ui.theme import CACHYCLI_THEME

_con = Console(theme=CACHYCLI_THEME)


@click.group(invoke_without_command=True)
@click.version_option(__version__, prog_name="cachycli")
@click.pass_context
def main(ctx: click.Context) -> None:
    """CachyCLI -- Learn Linux from your terminal, one lesson a day."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(lesson)


@main.command()
@click.argument("lesson_id", type=int, required=False)
def lesson(lesson_id: int | None = None) -> None:
    """Show a lesson. Defaults to the next uncompleted lesson."""
    db = ProgressDB()
    try:
        if lesson_id is None:
            lesson_id = next_lesson_id(db)
            if lesson_id is None:
                _con.print(
                    "[success]Congratulations! You have completed all 35 lessons![/success]"
                )
                return

        if lesson_id < 1 or lesson_id > TOTAL_LESSONS:
            _con.print(f"[error]Lesson id must be between 1 and {TOTAL_LESSONS}.[/error]")
            return

        les = load_lesson(lesson_id)
        render_lesson(les, _con)

        if not db.is_lesson_completed(lesson_id):
            db.complete_lesson(lesson_id)
            _con.print("[success]Lesson marked complete![/success]")

        _con.print("[info]Run [command]cachycli quiz[/command] to take the quiz.[/info]")
    finally:
        db.close()


@main.command()
@click.option("--weekly", "-w", is_flag=True, help="Take the weekly comprehensive quiz.")
@click.argument("target_id", type=int, required=False)
def quiz(weekly: bool = False, target_id: int | None = None) -> None:
    """Take a quiz. Defaults to the current lesson quiz."""
    db = ProgressDB()
    try:
        if weekly:
            week = target_id
            if week is None:
                lid = next_lesson_id(db)
                week = current_week(lid) if lid else 7
                # Offer the quiz for the most recent completed week.
                if lid and not is_week_complete(db, week):
                    week = max(1, week - 1) if week > 1 else 1
            try:
                q = load_weekly_quiz(week)
            except FileNotFoundError:
                _con.print(f"[error]Weekly quiz for week {week} not found.[/error]")
                return
        else:
            lid = target_id
            if lid is None:
                lid = next_lesson_id(db)
                if lid is None:
                    lid = TOTAL_LESSONS
                # If current lesson not yet completed, quiz for previous.
                if lid > 1 and not db.is_lesson_completed(lid):
                    lid = lid - 1

            try:
                q = load_lesson_quiz(lid)
            except FileNotFoundError:
                _con.print(f"[error]Quiz for lesson {lid} not found.[/error]")
                return

        score, total = run_quiz(q)
        db.record_quiz(q.quiz_type, q.quiz_id, score, total)
        pct = (score / total * 100) if total else 0
        if pct >= 70:
            _con.print(f"[success]Passed! {score}/{total} ({pct:.0f}%)[/success]")
        else:
            _con.print(f"[warning]Score: {score}/{total} ({pct:.0f}%). Need 70% to pass.[/warning]")
    finally:
        db.close()


@main.command()
def progress() -> None:
    """Show your progress dashboard."""
    db = ProgressDB()
    try:
        render_progress(db, _con)
    finally:
        db.close()


@main.command(name="list")
def list_lessons() -> None:
    """List all lessons with completion status."""
    db = ProgressDB()
    try:
        completed = set(db.completed_lesson_ids())
        lessons = load_all_lessons()
        current_wk = 0
        for les in lessons:
            if les.week != current_wk:
                current_wk = les.week
                _con.print(f"\n[heading]Week {current_wk}[/heading]")
            mark = "[success][check][/success]" if les.id in completed else "[muted][ ][/muted]"
            # Rich doesn't have [check] -- use a unicode checkmark.
            if les.id in completed:
                mark = "[success]\u2714[/success]"
            else:
                mark = "[muted]\u2610[/muted]"
            _con.print(f"  {mark}  Lesson {les.id:>2}: {les.title}")
    finally:
        db.close()


@main.command()
def sandbox() -> None:
    """Open an interactive sandbox for the current lesson."""
    db = ProgressDB()
    try:
        lid = next_lesson_id(db)
        if lid is None:
            lid = TOTAL_LESSONS
        les = load_lesson(lid)
        if not les.sandbox_commands:
            _con.print("[info]This lesson does not have sandbox exercises.[/info]")
            return

        from cachycli.utils.sandbox import Sandbox

        _con.print(
            f"[heading]Sandbox for Lesson {les.id}: {les.title}[/heading]"
        )
        _con.print(f"[info]Allowed commands: {', '.join(les.sandbox_commands)}[/info]")
        _con.print("[muted]Type 'exit' to leave the sandbox.[/muted]\n")

        with Sandbox(
            allowed_commands=les.sandbox_commands, setup_script=les.sandbox_setup
        ) as sb:
            while True:
                try:
                    cmd = input(f"sandbox:{sb.path}$ ")
                except (EOFError, KeyboardInterrupt):
                    break
                if cmd.strip().lower() in ("exit", "quit"):
                    break
                result = sb.run(cmd)
                if result.stdout:
                    _con.print(result.stdout, end="")
                if result.stderr:
                    _con.print(f"[error]{result.stderr}[/error]", end="")
    finally:
        db.close()


@main.command()
@click.confirmation_option(prompt="Are you sure you want to reset all progress?")
def reset() -> None:
    """Reset all progress."""
    db = ProgressDB()
    try:
        db.reset()
        _con.print("[warning]All progress has been reset.[/warning]")
    finally:
        db.close()
