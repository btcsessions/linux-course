"""Load YAML quiz files, present questions, score results."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Question:
    type: str  # "multiple_choice", "fill_in_blank", "true_false"
    question: str
    choices: list[str]  # Empty for fill_in_blank / true_false.
    answer: Any  # Index for MC, string for fill_in_blank, bool for TF.
    accept: list[str]  # Alternative accepted answers for fill_in_blank.
    explanation: str


@dataclass
class Quiz:
    quiz_type: str  # "lesson" or "weekly"
    quiz_id: str  # e.g. "lesson_01" or "week_01"
    questions: list[Question]


def _content_root() -> Path:
    here = Path(__file__).resolve()
    repo_root = here.parent.parent.parent.parent
    content = repo_root / "content"
    if content.is_dir():
        return content
    raise FileNotFoundError(f"Content directory not found at {content}")


def load_lesson_quiz(lesson_id: int) -> Quiz:
    week = (lesson_id - 1) // 5 + 1
    path = _content_root() / f"week{week:02d}" / f"lesson{lesson_id:02d}_quiz.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    return _parse_quiz(path, "lesson", f"lesson_{lesson_id:02d}")


def load_weekly_quiz(week: int) -> Quiz:
    path = _content_root() / f"week{week:02d}" / f"week{week:02d}_quiz.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Weekly quiz not found: {path}")
    return _parse_quiz(path, "weekly", f"week_{week:02d}")


def _parse_quiz(path: Path, quiz_type: str, quiz_id: str) -> Quiz:
    with open(path) as f:
        data = yaml.safe_load(f)

    questions: list[Question] = []
    for q in data.get("questions", []):
        questions.append(
            Question(
                type=q["type"],
                question=q["question"],
                choices=q.get("choices", []),
                answer=q["answer"],
                accept=q.get("accept", []),
                explanation=q.get("explanation", ""),
            )
        )
    return Quiz(quiz_type=quiz_type, quiz_id=quiz_id, questions=questions)


def check_answer(question: Question, user_answer: str) -> bool:
    """Return True if the user's answer is correct."""
    if question.type == "multiple_choice":
        try:
            return int(user_answer) == question.answer
        except (ValueError, TypeError):
            return False

    if question.type == "true_false":
        normalised = user_answer.strip().lower()
        if question.answer is True:
            return normalised in ("true", "t", "yes", "y", "1")
        return normalised in ("false", "f", "no", "n", "0")

    if question.type == "fill_in_blank":
        normalised = user_answer.strip().lower()
        accepted = [a.strip().lower() for a in question.accept] if question.accept else []
        if str(question.answer).strip().lower() not in accepted:
            accepted.append(str(question.answer).strip().lower())
        return normalised in accepted

    return False
