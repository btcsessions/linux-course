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
    _save_config_value("anthropic_api_key", key)


def get_update_remote() -> str:
    """Return the preferred git remote for updates."""
    if _CONFIG_FILE.exists():
        with open(_CONFIG_FILE, "rb") as f:
            data = tomllib.load(f)
        return data.get("update_remote", "origin")
    return "origin"


def save_update_remote(remote: str) -> None:
    """Save the preferred git remote for updates."""
    _save_config_value("update_remote", remote)


def _save_config_value(key: str, value: str | int | bool) -> None:
    """Save a single key to the config file."""
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    if _CONFIG_FILE.exists():
        with open(_CONFIG_FILE, "rb") as f:
            existing = tomllib.load(f)

    existing[key] = value

    lines: list[str] = []
    for k, v in existing.items():
        if isinstance(v, bool):
            lines.append(f"{k} = {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k} = {v}")
        else:
            lines.append(f'{k} = "{v}"')

    _CONFIG_FILE.write_text("\n".join(lines) + "\n")
