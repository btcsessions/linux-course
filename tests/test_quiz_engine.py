"""Tests for the quiz engine."""

import pytest

from cachycli.core.quiz_engine import Question, check_answer


def _mc(answer_idx=1):
    return Question(
        type="multiple_choice",
        question="What is 2+2?",
        choices=["3", "4", "5", "6"],
        answer=answer_idx,
        accept=[],
        explanation="Basic math.",
    )


def _tf(answer=True):
    return Question(
        type="true_false",
        question="The sky is blue.",
        choices=[],
        answer=answer,
        accept=[],
        explanation="It usually is.",
    )


def _fill(answer="date", accept=None):
    return Question(
        type="fill_in_blank",
        question="The command ___ shows the date.",
        choices=[],
        answer=answer,
        accept=accept or ["date"],
        explanation="The date command.",
    )


class TestMultipleChoice:
    def test_correct(self):
        assert check_answer(_mc(1), "1")

    def test_incorrect(self):
        assert not check_answer(_mc(1), "0")

    def test_non_numeric(self):
        assert not check_answer(_mc(1), "four")


class TestTrueFalse:
    def test_true_variants(self):
        q = _tf(True)
        for ans in ("true", "t", "yes", "y", "True", "TRUE", "1"):
            assert check_answer(q, ans), f"Failed for: {ans}"

    def test_false_variants(self):
        q = _tf(False)
        for ans in ("false", "f", "no", "n", "False", "FALSE", "0"):
            assert check_answer(q, ans), f"Failed for: {ans}"

    def test_wrong_answer(self):
        assert not check_answer(_tf(True), "false")
        assert not check_answer(_tf(False), "true")


class TestFillInBlank:
    def test_exact_match(self):
        assert check_answer(_fill(), "date")

    def test_case_insensitive(self):
        assert check_answer(_fill(), "Date")
        assert check_answer(_fill(), "DATE")

    def test_with_whitespace(self):
        assert check_answer(_fill(), "  date  ")

    def test_accepted_alternatives(self):
        q = _fill(answer="ls", accept=["ls", "ls -l"])
        assert check_answer(q, "ls")
        assert check_answer(q, "ls -l")

    def test_wrong_answer(self):
        assert not check_answer(_fill(), "time")
