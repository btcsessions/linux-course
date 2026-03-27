"""Tests for the lesson loader module."""

import pytest

from cachycli.core.lesson_loader import Lesson, load_all_lessons, load_lesson


def test_load_lesson_1():
    """Lesson 1 should load successfully with correct metadata."""
    les = load_lesson(1)
    assert les.id == 1
    assert les.week == 1
    assert les.title != ""
    assert len(les.objectives) >= 2
    assert len(les.commands) >= 1
    assert len(les.body) > 100  # Should have substantial content.


def test_load_lesson_invalid_id():
    with pytest.raises(FileNotFoundError):
        load_lesson(99)


def test_load_all_lessons():
    lessons = load_all_lessons()
    assert len(lessons) == 35
    # Check ordering.
    for i, les in enumerate(lessons):
        assert les.id == i + 1


def test_week_lesson_number():
    les = load_lesson(1)
    assert les.week_lesson_number == 1

    les = load_lesson(6)
    assert les.week_lesson_number == 1  # First lesson of week 2.

    les = load_lesson(10)
    assert les.week_lesson_number == 5  # Last lesson of week 2.
