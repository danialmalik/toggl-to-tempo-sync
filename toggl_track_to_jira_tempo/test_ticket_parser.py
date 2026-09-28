"""
Tests for ticket key detection (ticket_parser.py).
"""
import re

from ticket_parser import parse_description, DEFAULT_TICKET_PATTERNS


def default_patterns():
    return [re.compile(p, re.IGNORECASE) for p in DEFAULT_TICKET_PATTERNS]


def test_legacy_format():
    parsed = parse_description("NEW-123: Frontend bug fix task -- Worked on fixing the bug", default_patterns())
    assert parsed.ticket == "NEW-123"
    assert parsed.tempo_description == "Worked on fixing the bug"
    assert parsed.tickets == ["NEW-123"]


def test_legacy_format_without_separator():
    # Old code produced an empty tempo description here; must stay identical.
    parsed = parse_description("NEW-123: some work", default_patterns())
    assert parsed.ticket == "NEW-123"
    assert parsed.tempo_description == ""


def test_legacy_format_with_colon_inside_rest():
    parsed = parse_description("NEW-123: docs: updated -- done", default_patterns())
    assert parsed.ticket == "NEW-123"
    assert parsed.tempo_description == "done"


def test_ticket_anywhere_with_separator():
    parsed = parse_description("Worked on fixing the bug for NEW-123 -- done", default_patterns())
    assert parsed.ticket == "NEW-123"
    assert parsed.tempo_description == "done"


def test_ticket_anywhere_without_separator():
    parsed = parse_description("Worked on fixing NEW-123 now", default_patterns())
    assert parsed.ticket == "NEW-123"
    assert parsed.tempo_description == "Worked on fixing now"


def test_ticket_in_brackets():
    parsed = parse_description("[NEW-123] backend work", default_patterns())
    assert parsed.ticket == "NEW-123"
    assert parsed.tempo_description == "backend work"


def test_invalid_colon_prefix_falls_back_to_scan():
    # Old code derived the garbage key "refactor ZOL-6968" and failed validation.
    parsed = parse_description("refactor ZOL-6968: cleanup -- details", default_patterns())
    assert parsed.ticket == "ZOL-6968"
    assert parsed.tempo_description == "details"


def test_multiple_tickets():
    parsed = parse_description("NEW-1 + NEW-2 refactor", default_patterns())
    assert parsed.ticket is None
    assert parsed.tickets == ["NEW-1", "NEW-2"]
    assert parsed.tempo_description == "+ refactor"


def test_legacy_key_wins_over_other_tickets():
    # A colon-prefixed ticket is authoritative; no multi-ticket prompt.
    parsed = parse_description("NEW-1: work on NEW-2 too -- done", default_patterns())
    assert parsed.ticket == "NEW-1"
    assert parsed.tickets == ["NEW-1"]
    assert parsed.tempo_description == "done"


def test_no_ticket():
    parsed = parse_description("no ticket here", default_patterns())
    assert parsed.ticket is None
    assert parsed.tempo_description == ""
    assert parsed.tickets == []


def test_colon_prefix_that_is_not_ticket_and_no_ticket_elsewhere():
    parsed = parse_description("Refactor: cleanup", default_patterns())
    assert parsed.ticket is None
    assert parsed.tickets == []


def test_none_description():
    assert parse_description(None, default_patterns()).ticket is None
    assert parse_description("", default_patterns()).ticket is None


def test_lowercase_ticket_normalized():
    parsed = parse_description("worked on new-123 stuff", default_patterns())
    assert parsed.ticket == "NEW-123"


def test_word_boundaries_prevent_partial_matches():
    assert parse_description("preNEW-123", default_patterns()).ticket is None
    assert parse_description("NEW-123x", default_patterns()).ticket is None
    assert parse_description("NEW-123", default_patterns()).ticket == "NEW-123"


def test_custom_patterns_from_config():
    custom = [re.compile(r"(?<![A-Za-z0-9])[A-Z]{6}-\d+(?![A-Za-z0-9])", re.IGNORECASE)]
    # Default pattern (2-5 letters) does not match a 6-letter prefix.
    assert parse_description("ABCDEF-123 done", default_patterns()).ticket is None
    assert parse_description("ABCDEF-123 done", custom).ticket == "ABCDEF-123"
