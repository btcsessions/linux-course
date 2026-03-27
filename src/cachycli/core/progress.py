"""SQLite-backed progress tracking: lesson completions, quiz scores, streaks."""

from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import NamedTuple


def _default_db_path() -> Path:
    base = Path.home() / ".local" / "share" / "cachycli"
    base.mkdir(parents=True, exist_ok=True)
    return base / "progress.db"


_SCHEMA = """\
CREATE TABLE IF NOT EXISTS lessons_completed (
    lesson_id INTEGER PRIMARY KEY,
    completed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_type TEXT NOT NULL,
    quiz_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    percentage REAL NOT NULL,
    completed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS streaks (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_lesson_date TEXT
);
"""


class QuizResult(NamedTuple):
    quiz_type: str
    quiz_id: str
    score: int
    total: int
    percentage: float
    completed_at: str


class ProgressDB:
    def __init__(self, db_path: Path | None = None) -> None:
        self._path = db_path or _default_db_path()
        self._conn = sqlite3.connect(str(self._path))
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.executescript(_SCHEMA)
        # Ensure the singleton streaks row exists.
        self._conn.execute(
            "INSERT OR IGNORE INTO streaks (id, current_streak, longest_streak) "
            "VALUES (1, 0, 0)"
        )
        self._conn.commit()

    # -- Lessons ---------------------------------------------------------------

    def complete_lesson(self, lesson_id: int) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO lessons_completed (lesson_id, completed_at) "
            "VALUES (?, datetime('now'))",
            (lesson_id,),
        )
        self._conn.commit()
        self._update_streak()

    def is_lesson_completed(self, lesson_id: int) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM lessons_completed WHERE lesson_id = ?", (lesson_id,)
        ).fetchone()
        return row is not None

    def completed_lesson_ids(self) -> list[int]:
        rows = self._conn.execute(
            "SELECT lesson_id FROM lessons_completed ORDER BY lesson_id"
        ).fetchall()
        return [r[0] for r in rows]

    def completed_count(self) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) FROM lessons_completed"
        ).fetchone()
        return row[0] if row else 0

    # -- Quizzes ---------------------------------------------------------------

    def record_quiz(
        self, quiz_type: str, quiz_id: str, score: int, total: int
    ) -> None:
        pct = (score / total * 100) if total > 0 else 0.0
        self._conn.execute(
            "INSERT INTO quiz_results (quiz_type, quiz_id, score, total, percentage) "
            "VALUES (?, ?, ?, ?, ?)",
            (quiz_type, quiz_id, score, total, pct),
        )
        self._conn.commit()

    def best_quiz_result(self, quiz_type: str, quiz_id: str) -> QuizResult | None:
        row = self._conn.execute(
            "SELECT quiz_type, quiz_id, score, total, percentage, completed_at "
            "FROM quiz_results WHERE quiz_type = ? AND quiz_id = ? "
            "ORDER BY percentage DESC LIMIT 1",
            (quiz_type, quiz_id),
        ).fetchone()
        return QuizResult(*row) if row else None

    def weekly_quiz_passed(self, week: int) -> bool:
        result = self.best_quiz_result("weekly", f"week_{week:02d}")
        return result is not None and result.percentage >= 70.0

    def all_quiz_results(self) -> list[QuizResult]:
        rows = self._conn.execute(
            "SELECT quiz_type, quiz_id, score, total, percentage, completed_at "
            "FROM quiz_results ORDER BY completed_at DESC"
        ).fetchall()
        return [QuizResult(*r) for r in rows]

    # -- Streaks ---------------------------------------------------------------

    def _update_streak(self) -> None:
        today = date.today().isoformat()
        row = self._conn.execute(
            "SELECT current_streak, longest_streak, last_lesson_date FROM streaks WHERE id = 1"
        ).fetchone()
        current, longest, last_date = row

        if last_date == today:
            return  # Already counted today.

        yesterday = date.today().toordinal() - 1
        if last_date and date.fromisoformat(last_date).toordinal() == yesterday:
            current += 1
        else:
            current = 1

        longest = max(longest, current)
        self._conn.execute(
            "UPDATE streaks SET current_streak = ?, longest_streak = ?, last_lesson_date = ? "
            "WHERE id = 1",
            (current, longest, today),
        )
        self._conn.commit()

    def get_streak(self) -> tuple[int, int]:
        """Return (current_streak, longest_streak)."""
        row = self._conn.execute(
            "SELECT current_streak, longest_streak FROM streaks WHERE id = 1"
        ).fetchone()
        return (row[0], row[1]) if row else (0, 0)

    # -- Reset -----------------------------------------------------------------

    def reset(self) -> None:
        self._conn.executescript(
            "DELETE FROM lessons_completed; "
            "DELETE FROM quiz_results; "
            "UPDATE streaks SET current_streak=0, longest_streak=0, last_lesson_date=NULL WHERE id=1;"
        )

    def close(self) -> None:
        self._conn.close()
