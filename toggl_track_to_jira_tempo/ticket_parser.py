"""
Ticket key detection for Toggl entry descriptions.

Descriptions may use the legacy format:
    <ISSUE_KEY>: <general notes> -- <tempo description>

or the ticket key may appear anywhere in the description, detected via
regex patterns from config.json ("ticket_patterns"). When the config key
is absent, a default JIRA-style key pattern is used.
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional

from config import config

DEFAULT_TICKET_PATTERNS = [
    r"(?<![A-Za-z0-9])[A-Z]{2,5}-\d{1,6}(?![A-Za-z0-9])",
]


@dataclass
class ParsedDescription:
    ticket: Optional[str]       # resolved single ticket (legacy or only match)
    tempo_description: str       # what gets sent to Tempo as the worklog description
    tickets: List[str] = field(default_factory=list)  # all matches (multiple-ticket case)


def get_ticket_patterns() -> List[re.Pattern]:
    """Compile ticket patterns from config, falling back to the default."""
    raw_patterns = getattr(config, "ticket_patterns", None) or DEFAULT_TICKET_PATTERNS
    compiled = []
    for pattern in raw_patterns:
        try:
            compiled.append(re.compile(pattern, re.IGNORECASE))
        except re.error as e:
            raise ValueError(f"Invalid ticket_patterns entry {pattern!r} in config.json: {e}")
    return compiled


def _tempo_description_after_separator(description: str) -> str:
    """Legacy rule: text after the first '--', or empty (byte-compatible with old code)."""
    return ("--" in description and description.split("--")[1] or "").strip()


def _strip_tickets(description: str, spans) -> str:
    """Remove matched ticket tokens (and any wrapping bracket/paren pair) from
    the description and collapse leftover whitespace."""
    parts = []
    last = 0
    for start, end in sorted(spans):
        if start < last:
            continue  # overlapping spans from multiple patterns
        if start > 0 and end < len(description):
            if (description[start - 1], description[end]) in (("[", "]"), ("(", ")")):
                start -= 1
                end += 1
        parts.append(description[last:start])
        last = end
    parts.append(description[last:])
    return re.sub(r"\s{2,}", " ", "".join(parts)).strip()


def parse_description(description: Optional[str], patterns=None) -> ParsedDescription:
    """
    Extract ticket key(s) and the Tempo worklog description from a Toggl entry.

    - Legacy format ("KEY: ... -- ...") is parsed byte-identically to the old
      code so previously synced entries hash the same way in SyncTracker.
    - Otherwise the whole description is scanned; the first ticket wins, or all
      matches are returned when multiple are found.
    """
    patterns = patterns if patterns is not None else get_ticket_patterns()

    if not description:
        return ParsedDescription(ticket=None, tempo_description="", tickets=[])

    # Legacy rule: "KEY: <rest>": the key must sit left of the first colon and
    # look like a ticket. Otherwise the description is scanned as a whole.
    if ":" in description:
        prefix = description.split(":")[0].strip()
        if any(pattern.fullmatch(prefix) for pattern in patterns):
            return ParsedDescription(
                ticket=prefix,
                tempo_description=_tempo_description_after_separator(description),
                tickets=[prefix],
            )

    matches = []
    seen = set()
    for pattern in patterns:
        for m in pattern.finditer(description):
            key = m.group(0).upper()
            if key not in seen:
                seen.add(key)
                matches.append((m.span(), key))
    matches.sort(key=lambda t: t[0])

    tickets = [key for _, key in matches]
    if not tickets:
        return ParsedDescription(ticket=None, tempo_description="", tickets=[])

    if "--" in description:
        tempo_description = _tempo_description_after_separator(description)
    else:
        tempo_description = _strip_tickets(description, [span for span, _ in matches])

    return ParsedDescription(
        ticket=tickets[0] if len(tickets) == 1 else None,
        tempo_description=tempo_description,
        tickets=tickets,
    )
