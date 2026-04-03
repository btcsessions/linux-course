"""Load/save user configuration (TOML)."""

from __future__ import annotations

import os
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


def get_api_key() -> str:
    """Return the Anthropic API key from config file or environment."""
    # Environment variable takes priority.
    env_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if env_key:
        return env_key

    if _CONFIG_FILE.exists():
        with open(_CONFIG_FILE, "rb") as f:
            data = tomllib.load(f)
        return data.get("anthropic_api_key", "")
    return ""


def save_api_key(key: str) -> None:
    """Save the Anthropic API key to the config file."""
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing config if present.
    existing: dict = {}
    if _CONFIG_FILE.exists():
        with open(_CONFIG_FILE, "rb") as f:
            existing = tomllib.load(f)

    existing["anthropic_api_key"] = key

    # Write back as TOML (simple key=value, no third-party writer needed).
    lines: list[str] = []
    for k, v in existing.items():
        if isinstance(v, bool):
            lines.append(f"{k} = {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k} = {v}")
        else:
            lines.append(f'{k} = "{v}"')

    _CONFIG_FILE.write_text("\n".join(lines) + "\n")
