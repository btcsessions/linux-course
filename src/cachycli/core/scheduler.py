"""Determine which lesson the user should do next."""

from __future__ import annotations

from cachycli.core.progress import ProgressDB

TOTAL_LESSONS = 35
LESSONS_PER_WEEK = 5


def next_lesson_id(db: ProgressDB) -> int | None:
    """Return the id of the next uncompleted lesson, or None if all done."""
    completed = set(db.completed_lesson_ids())
    for lid in range(1, TOTAL_LESSONS + 1):
        if lid not in completed:
            return lid
    return None


def current_week(lesson_id: int) -> int:
    return (lesson_id - 1) // LESSONS_PER_WEEK + 1


def week_progress(db: ProgressDB, week: int) -> tuple[int, int]:
    """Return (completed_in_week, total_in_week)."""
    start = (week - 1) * LESSONS_PER_WEEK + 1
    end = start + LESSONS_PER_WEEK
    completed = set(db.completed_lesson_ids())
    done = sum(1 for lid in range(start, end) if lid in completed)
    return done, LESSONS_PER_WEEK


def is_week_complete(db: ProgressDB, week: int) -> bool:
    done, total = week_progress(db, week)
    return done == total
