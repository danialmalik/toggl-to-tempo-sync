"""
Tests for the interactive choice UI (ui.py) — non-TTY fallback path.
Interactive arrow-key behavior needs a real pty and is covered by a smoke test.
"""
import builtins

import sync
from sync import input_choice


def test_input_choice_numeric_fallback(monkeypatch):
    """When interactive UI is unavailable, numeric selection still works."""
    monkeypatch.setattr(sync, "interactive_available", lambda: False)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "2")

    assert input_choice("Choose", ["alpha", "beta", "gamma"]) == "beta"


def test_input_choice_numeric_fallback_invalid(monkeypatch):
    """Invalid numeric input recurses until a valid choice."""
    answers = iter(["99", "3"])
    monkeypatch.setattr(sync, "interactive_available", lambda: False)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(answers))

    assert input_choice("Choose", ["alpha", "beta", "gamma"]) == "gamma"
