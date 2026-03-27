"""Load/save user configuration (TOML)."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


_CONFIG_DIR = Path.home() / ".config" / "cachycli"
_CONFIG_FILE = _CONFIG_DIR / "config.toml"

_DEFAULTS = {
    "theme": "dark",
    "paging": "sequential",  # "sequential" or "free"
    "pass_threshold": 70,
}


@dataclass
class Config:
    theme: str
    paging: str
    pass_threshold: int


def load_config() -> Config:
    if _CONFIG_FILE.exists():
        with open(_CONFIG_FILE, "rb") as f:
            data = tomllib.load(f)
    else:
        data = {}

    return Config(
        theme=data.get("theme", _DEFAULTS["theme"]),
        paging=data.get("paging", _DEFAULTS["paging"]),
        pass_threshold=data.get("pass_threshold", _DEFAULTS["pass_threshold"]),
    )
