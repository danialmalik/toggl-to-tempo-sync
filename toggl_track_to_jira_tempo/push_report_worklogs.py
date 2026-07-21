"""
One-off backfill: push the reconciled day-by-day rows from
tempo_time_log_report_2026-07.md to Tempo as real worklogs.

This is deliberately separate from sync.py: sync.py drives worklogs directly
off raw Toggl entries (1 entry -> 1 issue via "ISSUE-KEY: description").
This report's rows are the *output* of a manual reconciliation (split,
redistributed, merged, rounded) -- there's no 1:1 Toggl entry to replay, so
we source rows straight from the markdown table (the thing you actually
reviewed and approved) and post each row as its own Tempo worklog.

Usage:
    python push_report_worklogs.py                 # dry run (default), prints what would be posted
    python push_report_worklogs.py --live           # actually posts to Tempo
    python push_report_worklogs.py --live --only ZOL-6968,ZOL-7394   # restrict to specific tickets

Idempotency: every successful post is appended to push_report_worklogs.log.json
next to this file. Re-running (even with --live) skips rows already recorded
there (matched on date+ticket+type+hours+description), so a crash/partial
run can be safely re-run.
"""
import os
import re
import sys
import json
import hashlib
from collections import defaultdict

from config import config
from jira_api import JiraAPI
from jira_tempo_api import JiraTempoAPI

REPORT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tempo_time_log_report_2026-07.md",
)
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "push_report_worklogs.log.json")

ROW_RE = re.compile(
    r"^\|\s*(?P<date>[\d-]{10}|—)\s*\|\s*(?P<ticket>[A-Z]+-\d+)\s*\|\s*(?P<type>[\w-]+)\s*\|\s*(?P<hours>[\d.]+)h\s*\|\s*(?P<notes>.*?)\s*\|\s*$"
)


def parse_report_rows(path=REPORT_PATH):
    """Extract (date, ticket, type, hours, notes) from the day-by-day table."""
    with open(path) as f:
        text = f.read()

    lines = text.splitlines()
    in_table = False
    rows = []
    for line in lines:
        if line.startswith("| Date | Ticket | Type | Hours"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        if line.startswith("|---"):
            continue
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        date = m.group("date")
        hours = float(m.group("hours"))
        if date == "—" or hours == 0:
            continue  # explicitly-excluded / zero-hour rows (ZOL-6961 etc.)
        notes = clean_notes(m.group("notes"))
        rows.append({
            "date": date,
            "ticket": m.group("ticket"),
            "type": m.group("type"),
            "hours": hours,
            "notes": notes,
        })
    return rows


def clean_notes(notes: str) -> str:
    notes = notes.replace("`", "")
    notes = re.sub(r"\*\*(.*?)\*\*", r"\1", notes)
    return notes.strip()


def row_key(row: dict) -> str:
    raw = f"{row['date']}|{row['ticket']}|{row['type']}|{row['hours']}|{row['notes']}"
    return hashlib.sha256(raw.encode()).hexdigest()


def load_log() -> dict:
    if not os.path.exists(LOG_PATH):
        return {}
    with open(LOG_PATH) as f:
        return json.load(f)


def save_log(log: dict):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2, sort_keys=True)


def main():
    live = "--live" in sys.argv
    only = None
    for arg in sys.argv:
        if arg.startswith("--only"):
            value = arg.split("=", 1)[1] if "=" in arg else sys.argv[sys.argv.index(arg) + 1]
            only = set(t.strip() for t in value.split(","))

    rows = parse_report_rows()
    if only:
        rows = [r for r in rows if r["ticket"] in only]

    print(f"Parsed {len(rows)} rows from {os.path.basename(REPORT_PATH)}")
    print(f"Total hours in scope: {sum(r['hours'] for r in rows):.2f}h")
    print(f"Mode: {'LIVE (will post to Tempo)' if live else 'DRY RUN (nothing will be posted)'}")
    print()

    log = load_log()

    jira_api = JiraAPI(
        subdomain=config.jira.subdomain,
        user_email=config.jira.user_email,
        api_token=config.jira.api_token,
    )
    jira_tempo_api = JiraTempoAPI(account_id=config.tempo.user_id, auth_token=config.tempo.api_key)

    issue_id_cache = {}
    posted, skipped, failed = 0, 0, 0
    by_ticket_posted = defaultdict(float)

    for row in sorted(rows, key=lambda r: (r["date"], r["ticket"])):
        key = row_key(row)
        label = f"{row['date']} | {row['ticket']:10s} | {row['type']:11s} | {row['hours']:.2f}h | {row['notes'][:90]}"

        if key in log:
            print(f"SKIP (already logged, tempoWorklogId={log[key].get('tempo_worklog_id')}): {label}")
            skipped += 1
            continue

        if not live:
            print(f"WOULD POST: {label}")
            continue

        try:
            if row["ticket"] not in issue_id_cache:
                issue_details = jira_api.get_issue_details(row["ticket"])
                issue_id_cache[row["ticket"]] = issue_details["id"]

            issue_id = issue_id_cache[row["ticket"]]
            description = f"[{row['type']}] {row['notes']}"
            result = jira_tempo_api.add_worklog(
                issue_id=issue_id,
                time_spent_seconds=int(round(row["hours"] * 3600)),
                start_date=row["date"],
                description=description,
            )
            tempo_worklog_id = result.get("tempoWorklogId") if isinstance(result, dict) else None
            log[key] = {
                **row,
                "issue_id": issue_id,
                "tempo_worklog_id": tempo_worklog_id,
            }
            save_log(log)
            by_ticket_posted[row["ticket"]] += row["hours"]
            posted += 1
            print(f"POSTED (tempoWorklogId={tempo_worklog_id}): {label}")
        except Exception as e:
            error_message = e.response.text if hasattr(e, "response") and e.response is not None else str(e)
            failed += 1
            print(f"FAILED: {label}\n   -> {error_message[:300]}")

    print()
    print(f"Done. posted={posted} skipped(already logged)={skipped} failed={failed} dry_run_rows={0 if live else len(rows)}")
    if live and posted:
        print("Posted hours by ticket:")
        for t, h in sorted(by_ticket_posted.items(), key=lambda kv: -kv[1]):
            print(f"  {t}: {h:.2f}h")


if __name__ == "__main__":
    main()
