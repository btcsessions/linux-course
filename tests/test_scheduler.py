"""Tests for the scheduler module."""

import pytest

from cachycli.core.progress import ProgressDB
from cachycli.core.scheduler import (
    current_week,
    is_week_complete,
    next_lesson_id,
    week_progress,
)


@pytest.fixture
def db(tmp_path):
    d = ProgressDB(tmp_path / "test.db")
    yield d
    d.close()


def test_next_lesson_id_fresh(db):
    assert next_lesson_id(db) == 1


def test_next_lesson_id_after_completing(db):
    db.complete_lesson(1)
    db.complete_lesson(2)
    assert next_lesson_id(db) == 3


def test_next_lesson_id_all_done(db):
    for i in range(1, 36):
        db.complete_lesson(i)
    assert next_lesson_id(db) is None


def test_current_week():
    assert current_week(1) == 1
    assert current_week(5) == 1
    assert current_week(6) == 2
    assert current_week(10) == 2
    assert current_week(35) == 7


def test_week_progress(db):
    done, total = week_progress(db, 1)
    assert done == 0
    assert total == 5

    db.complete_lesson(1)
    db.complete_lesson(3)
    done, total = week_progress(db, 1)
    assert done == 2
    assert total == 5


def test_is_week_complete(db):
    assert not is_week_complete(db, 1)
    for i in range(1, 6):
        db.complete_lesson(i)
    assert is_week_complete(db, 1)
    assert not is_week_complete(db, 2)
