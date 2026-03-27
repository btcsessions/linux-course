"""Tests for the progress tracking module."""

import tempfile
from pathlib import Path

import pytest

from cachycli.core.progress import ProgressDB


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test_progress.db"
    d = ProgressDB(db_path)
    yield d
    d.close()


def test_complete_lesson(db):
    assert not db.is_lesson_completed(1)
    db.complete_lesson(1)
    assert db.is_lesson_completed(1)


def test_completed_lesson_ids(db):
    db.complete_lesson(3)
    db.complete_lesson(1)
    db.complete_lesson(5)
    assert db.completed_lesson_ids() == [1, 3, 5]


def test_completed_count(db):
    assert db.completed_count() == 0
    db.complete_lesson(1)
    db.complete_lesson(2)
    assert db.completed_count() == 2


def test_record_quiz(db):
    db.record_quiz("lesson", "lesson_01", 4, 5)
    result = db.best_quiz_result("lesson", "lesson_01")
    assert result is not None
    assert result.score == 4
    assert result.total == 5
    assert result.percentage == 80.0


def test_best_quiz_result_picks_highest(db):
    db.record_quiz("lesson", "lesson_01", 3, 5)
    db.record_quiz("lesson", "lesson_01", 5, 5)
    db.record_quiz("lesson", "lesson_01", 4, 5)
    result = db.best_quiz_result("lesson", "lesson_01")
    assert result.score == 5
    assert result.percentage == 100.0


def test_weekly_quiz_passed(db):
    assert not db.weekly_quiz_passed(1)
    db.record_quiz("weekly", "week_01", 10, 15)
    assert not db.weekly_quiz_passed(1)  # 66.7% < 70%
    db.record_quiz("weekly", "week_01", 11, 15)
    assert db.weekly_quiz_passed(1)  # 73.3% >= 70%


def test_streak_increments(db):
    db.complete_lesson(1)
    current, longest = db.get_streak()
    assert current == 1
    assert longest == 1


def test_reset(db):
    db.complete_lesson(1)
    db.record_quiz("lesson", "lesson_01", 5, 5)
    db.reset()
    assert db.completed_count() == 0
    assert db.best_quiz_result("lesson", "lesson_01") is None
    current, longest = db.get_streak()
    assert current == 0
    assert longest == 0
