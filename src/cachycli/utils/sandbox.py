"""Safe command execution sandbox for lesson practice exercises.

Creates a temporary directory with sample files, runs whitelisted commands
with a timeout, and cleans up afterwards.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Commands that are NEVER allowed regardless of lesson whitelist.
_BLACKLIST = frozenset({
    "sudo", "su", "dd", "mkfs", "fdisk", "parted",
    "reboot", "shutdown", "poweroff", "halt", "init",
    "rm -rf /", "rm -rf /*",
})

# Maximum output length returned to the TUI (bytes).
_MAX_OUTPUT = 8192

# Default timeout per command (seconds).
_TIMEOUT = 5


@dataclass
class SandboxResult:
    command: str
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool = False


class Sandbox:
    """A temporary sandbox directory for safe command practice."""

    def __init__(
        self,
        allowed_commands: list[str] | None = None,
        setup_script: str = "",
    ) -> None:
        self._allowed = set(allowed_commands) if allowed_commands else None
        self._setup_script = setup_script
        self._tmpdir: str | None = None

    def __enter__(self) -> "Sandbox":
        self._tmpdir = tempfile.mkdtemp(prefix="cachycli-sandbox-")
        if self._setup_script:
            subprocess.run(
                ["bash", "-c", self._setup_script],
                cwd=self._tmpdir,
                timeout=10,
                capture_output=True,
            )
        return self

    def __exit__(self, *exc: object) -> None:
        if self._tmpdir and os.path.isdir(self._tmpdir):
            shutil.rmtree(self._tmpdir, ignore_errors=True)
        self._tmpdir = None

    @property
    def path(self) -> str:
        if not self._tmpdir:
            raise RuntimeError("Sandbox not entered. Use as a context manager.")
        return self._tmpdir

    def run(self, command: str) -> SandboxResult:
        """Execute *command* inside the sandbox directory."""
        if not self._tmpdir:
            raise RuntimeError("Sandbox not entered. Use as a context manager.")

        stripped = command.strip()

        # Safety: reject blacklisted commands.
        base_cmd = stripped.split()[0] if stripped else ""
        if base_cmd in _BLACKLIST or stripped in _BLACKLIST:
            return SandboxResult(
                command=command,
                stdout="",
                stderr=f"Command not allowed in sandbox: {base_cmd}",
                returncode=1,
            )

        # Safety: check whitelist if set.
        if self._allowed is not None and base_cmd not in self._allowed:
            return SandboxResult(
                command=command,
                stdout="",
                stderr=(
                    f"Command '{base_cmd}' is not in this lesson's allowed commands.\n"
                    f"Allowed: {', '.join(sorted(self._allowed))}"
                ),
                returncode=1,
            )

        try:
            proc = subprocess.run(
                ["bash", "-c", stripped],
                cwd=self._tmpdir,
                capture_output=True,
                text=True,
                timeout=_TIMEOUT,
                env=_sandbox_env(self._tmpdir),
            )
            return SandboxResult(
                command=command,
                stdout=proc.stdout[:_MAX_OUTPUT],
                stderr=proc.stderr[:_MAX_OUTPUT],
                returncode=proc.returncode,
            )
        except subprocess.TimeoutExpired:
            return SandboxResult(
                command=command,
                stdout="",
                stderr="Command timed out (5 second limit).",
                returncode=1,
                timed_out=True,
            )


def _sandbox_env(tmpdir: str) -> dict[str, str]:
    """Build a restricted environment for sandbox commands."""
    return {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": tmpdir,
        "TERM": os.environ.get("TERM", "xterm-256color"),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }
