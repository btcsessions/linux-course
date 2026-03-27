"""Load lesson markdown files with YAML frontmatter."""

from __future__ import annotations

import importlib.resources
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter


@dataclass
class Lesson:
    id: int
    week: int
    title: str
    duration_minutes: int
    objectives: list[str]
    commands: list[str]
    prerequisites: list[int]
    sandbox_commands: list[str]
    sandbox_setup: str
    body: str  # Markdown content after frontmatter.

    @property
    def week_lesson_number(self) -> int:
        """Lesson number within its week (1-based)."""
        return self.id - (self.week - 1) * 5


def _content_root() -> Path:
    """Return the content/ directory at the repo root."""
    # Walk up from this file: src/cachycli/core/lesson_loader.py -> repo root
    here = Path(__file__).resolve()
    repo_root = here.parent.parent.parent.parent
    content = repo_root / "content"
    if content.is_dir():
        return content
    raise FileNotFoundError(f"Content directory not found at {content}")


def load_lesson(lesson_id: int) -> Lesson:
    """Load a single lesson by its global id (1-35)."""
    week = (lesson_id - 1) // 5 + 1
    lesson_in_week = (lesson_id - 1) % 5 + 1
    path = _content_root() / f"week{week:02d}" / f"lesson{lesson_id:02d}.md"
    if not path.exists():
        raise FileNotFoundError(f"Lesson file not found: {path}")
    return _parse_lesson(path)


def load_all_lessons() -> list[Lesson]:
    """Load all lessons in order."""
    lessons: list[Lesson] = []
    content = _content_root()
    for week_dir in sorted(content.iterdir()):
        if not week_dir.is_dir() or not week_dir.name.startswith("week"):
            continue
        for md_file in sorted(week_dir.glob("lesson*.md")):
            lessons.append(_parse_lesson(md_file))
    return lessons


def _parse_lesson(path: Path) -> Lesson:
    post = frontmatter.load(str(path))
    meta = post.metadata
    return Lesson(
        id=meta["id"],
        week=meta["week"],
        title=meta["title"],
        duration_minutes=meta.get("duration_minutes", 15),
        objectives=meta.get("objectives", []),
        commands=meta.get("commands", []),
        prerequisites=meta.get("prerequisites", []),
        sandbox_commands=meta.get("sandbox_commands", []),
        sandbox_setup=meta.get("sandbox_setup", ""),
        body=post.content,
    )
