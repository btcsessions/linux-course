"""Tests for the sandbox module."""

import pytest

from cachycli.utils.sandbox import Sandbox


def test_basic_command():
    with Sandbox(allowed_commands=["echo", "ls"]) as sb:
        result = sb.run("echo hello")
        assert result.returncode == 0
        assert "hello" in result.stdout


def test_blocked_command():
    with Sandbox(allowed_commands=["echo"]) as sb:
        result = sb.run("rm -rf /tmp/test")
        assert result.returncode == 1
        assert "not in this lesson" in result.stderr


def test_blacklisted_command():
    with Sandbox(allowed_commands=["sudo"]) as sb:
        result = sb.run("sudo ls")
        assert result.returncode == 1
        assert "not allowed" in result.stderr.lower()


def test_sandbox_setup():
    with Sandbox(
        allowed_commands=["ls", "cat"],
        setup_script="echo 'test content' > testfile.txt",
    ) as sb:
        result = sb.run("cat testfile.txt")
        assert result.returncode == 0
        assert "test content" in result.stdout


def test_sandbox_cleanup():
    path = None
    with Sandbox() as sb:
        path = sb.path
        sb.run("touch keepme.txt")
    import os
    assert not os.path.exists(path)


def test_no_whitelist_allows_safe_commands():
    with Sandbox() as sb:
        result = sb.run("echo works")
        assert result.returncode == 0
        assert "works" in result.stdout
