import os
import datetime
from collections import defaultdict
from typing import Optional

import requests
from jira_api import JiraAPI
from toggle_api import TogglTrackAPI
from jira_tempo_api import JiraTempoAPI
from sync_tracker import SyncTracker
from animated_progress import SyncProgressDisplay, create_api_loader
from pprint import pprint
from config import config
from utils import Logger


TOGGL_TRACK_AUTH_TOKEN = config.toggl.api_key
JIRA_TEMPO_AUTH_TOKEN = config.tempo.api_key
JIRA_TEMPO_ACCOUNT_ID = config.tempo.user_id


def confirm(message: str):
    Logger.log_info(message)

    confirm_prompt = Logger.format_message("Confirm? [y/n]: ", Logger.INFO_SECONDARY)
    Logger.log_info_raw(confirm_prompt)
    return input(f"{message} [y/n]: ").lower().strip() == "y"

def input_choice(prompt: str, choices: list):
    Logger.log_info(prompt)
    for i, choice in enumerate(choices):
        choice_formatted = Logger.format_message(choice, Logger.INFO_SECONDARY)
        Logger.log_info(f"{i+1}. {choice_formatted}")

    choice = input(f"Enter choice [1-{len(choices)}]: ")
    try:
        return choices[int(choice)-1]
    except (ValueError, IndexError, KeyError):
        Logger.log_error("Invalid choice. Please try again.")
        return input_choice(prompt, choices)

def wait_for_enter(msg: str):
    formatted_msg = Logger.format_message(f"{msg}. Press enter to continue...", Logger.INFO_SECONDARY)
    input(formatted_msg)

def seconds_to_human_readable(seconds: int):
    return str(datetime.timedelta(seconds=seconds))

def input_or_default(prompt: str, default: str):
    default_formatted = Logger.format_message(default, Logger.INFO_SECONDARY)
    value = input(f"{prompt} [{default_formatted}]: ")
    return value or default

def sync(start_date: str, end_date: Optional[str] = None, round_seconds: int = 60, residual_ticket: Optional[str] = None):
    """
    Sync Toggl time entries to Jira Tempo.

    Note: When manual entry corrections are made during sync failures,
    the sync record is created using the ORIGINAL Toggl entry details.
    This prevents the same Toggl entry from being processed again in future syncs,
    even if the user modified the details before successful upload.
    """
    toggl_api = TogglTrackAPI(auth_token=TOGGL_TRACK_AUTH_TOKEN)
    jira_tempo_api = JiraTempoAPI(account_id=JIRA_TEMPO_ACCOUNT_ID, auth_token=JIRA_TEMPO_AUTH_TOKEN)
    jira_api = JiraAPI(
        subdomain=config.jira.subdomain,
        user_email=config.jira.user_email,
        api_token=config.jira.api_token
    )

    # Initialize sync tracker
    sync_tracker = SyncTracker()

    # Fetch raw (unrounded) entries. Rounding is applied locally so we retain
    # both raw and rounded durations for day-level residual reconciliation.
    with create_api_loader("Fetching Toggl entries") as loader:
        entries = toggl_api.get_time_entries(
            start_date=start_date,
            end_date=end_date,
            group=True,
            round_seconds_to=0,
            # skip_entry_substr="SKIP",
            exclude_tags=["banked_hours", "unpaid", "skip_tempo"],
            exclude_projects=["Hours Bank"],
        )

    for entry in entries:
        entry["raw_duration"] = entry["duration"]
        entry["duration"] = round(entry["duration"] / round_seconds) * round_seconds

    # Per-day raw vs logged totals, used to recover time lost to rounding.
    day_raw_totals = defaultdict(int)
    day_logged_totals = defaultdict(int)
    day_synced_keys = defaultdict(list)

    total_entries = len(entries)

    # Initialize progress display
    progress = SyncProgressDisplay(total_entries)
    progress.print_header()

    for entry in entries:
        # Store original entry details for sync tracking
        original_issue_key = entry["description"].split(":")[0].strip()
        original_issue_description = "--" in entry["description"] and entry["description"].split("--")[1] or ""
        original_issue_description = original_issue_description.strip()
        original_duration = entry["duration"]
        raw_duration = entry["raw_duration"]
        datetime_obj = datetime.datetime.strptime(entry["start"], "%Y-%m-%dT%H:%M:%S+00:00")
        original_entry_date = datetime_obj.date()
        original_entry_date_str = str(original_entry_date)

        # Working variables that may be modified by user input
        issue_key = original_issue_key
        issue_description = original_issue_description
        duration = original_duration
        entry_date_str = original_entry_date_str

        # Format display strings
        duration_formatted = seconds_to_human_readable(duration)

        # Entries that round to 0 (e.g. <half the rounding window) aren't logged
        # individually; their raw time is recovered via the day-level residual.
        if duration == 0:
            progress.show_entry_user_skipped("rounded to 0; recovered as residual")
            day_raw_totals[entry_date_str] += raw_duration
            continue

        # Show entry processing start
        progress.start_entry_processing(issue_key, duration_formatted, entry_date_str)

        # Get original Toggl IDs (either from grouped entry or single entry)
        original_toggl_ids = entry.get("original_toggl_ids", [entry["id"]])

        # Check if this entry has already been synced (using original details)
        if sync_tracker.is_entry_synced(
            toggl_ids=original_toggl_ids,
            issue_key=original_issue_key,
            description=original_issue_description,
            duration=original_duration,
            start_date=original_entry_date_str
        ):
            progress.show_entry_skipped(issue_key)
            continue

        while True:
            try:
                # Get issue details with loading animation
                with create_api_loader("Validating JIRA issue") as loader:
                    issue_details = jira_api.get_issue_details(issue_key)
                    issue_id = issue_details["id"]
                    issue_summary = issue_details.get("fields", {}).get("summary", "")

                progress.show_api_activity(f"Issue: {issue_summary}")

                # Check if issue summary contains "Moved to" or "not in use" (case insensitive)
                if issue_summary and ("moved to" in issue_summary.lower() or "not in use" in issue_summary.lower()):
                    warning_text = Logger.format_message("WARNING: This issue appears to be deprecated or moved.", Logger.WARNING)
                    Logger.log_warning(warning_text)

                    options = ["Continue Anyway", "Modify Details", "Skip"]
                    choice = input_choice("Issue may be deprecated or moved. Choose an option:", options)

                    if choice == "Skip":
                        progress.show_entry_user_skipped("user skipped (deprecated issue)")
                        break
                    elif choice == "Modify Details":
                        issue_key = input_or_default("Issue key", issue_key)
                        duration = int(input_or_default("Time spent (seconds)", str(duration)))
                        entry_date_str = input_or_default("Start date (YYYY-MM-DD)", entry_date_str)
                        issue_description = input_or_default("Description", issue_description)
                        continue

                # Add worklog to Tempo with loading animation
                with create_api_loader("Syncing to Tempo") as loader:
                    worklog_result = jira_tempo_api.add_worklog(
                        issue_id=issue_id,
                        time_spent_seconds=duration,
                        start_date=entry_date_str,
                        description=issue_description
                    )

                # Record successful sync using ORIGINAL entry details to prevent re-processing
                # This ensures that even if user manually modified details, the original Toggl entry won't be synced again
                tempo_worklog_id = worklog_result.get("tempoWorklogId") if isinstance(worklog_result, dict) else None
                sync_tracker.record_sync(
                    toggl_ids=original_toggl_ids,
                    issue_key=original_issue_key,
                    description=original_issue_description,
                    duration=original_duration,
                    start_date=original_entry_date_str,
                    tempo_worklog_id=tempo_worklog_id,
                    additional_data={
                        "issue_id": issue_id,
                        "issue_summary": issue_summary,
                        "sync_date_range": f"{start_date} to {end_date or start_date}",
                        "manually_modified": original_issue_key != issue_key or original_duration != duration or original_entry_date_str != entry_date_str,
                        "actual_synced_details": {
                            "issue_key": issue_key,
                            "description": issue_description,
                            "duration": duration,
                            "start_date": entry_date_str
                        } if (original_issue_key != issue_key or original_duration != duration or original_entry_date_str != entry_date_str) else None
                    }
                )

                # Account logged time for day-level residual reconciliation.
                day_raw_totals[entry_date_str] += raw_duration
                day_logged_totals[entry_date_str] += duration
                day_synced_keys[entry_date_str].append(issue_key)

                progress.show_entry_success()
                break

            except Exception as e:
                if isinstance(e, requests.exceptions.HTTPError):
                    error_message = e.response.text
                else:
                    error_message = str(e)

                progress.show_entry_failed(f"API Error: {str(e)[:100]}...")

                # Format variables for interactive prompts
                issue_key_formatted = Logger.format_message(issue_key, Logger.INFO_SECONDARY)
                error_formatted = Logger.format_message(error_message, Logger.ERROR)
                Logger.log_error(f"Failed to add worklog for {issue_key_formatted}: {error_formatted}")

                options = ["Retry", "Skip", "Manual Entry", "Open JIRA Issue", "Exit"]
                choice = input_choice("Choose an option:", options)

                if choice == "Retry":
                    Logger.log_info(f"Retrying worklog for {issue_key_formatted}...")
                    continue

                elif choice == "Skip":
                    progress.show_entry_user_skipped("user choice")
                    break

                elif choice == "Exit":
                    progress.print_summary()
                    exit(1)

                elif choice == "Manual Entry":
                    Logger.log_info(Logger.format_message("Entering manual correction mode:", Logger.INFO))
                    issue_key = input_or_default("Issue key", issue_key)
                    duration = int(input_or_default("Time spent (seconds)", str(duration)))
                    entry_date_str = input_or_default("Start date (YYYY-MM-DD)", entry_date_str)
                    issue_description = input_or_default("Description", issue_description)
                    Logger.log_info(Logger.format_message("Note: Sync record will use original Toggl entry details to prevent duplicate processing.", Logger.INFO_SECONDARY))
                    continue

                elif choice == "Open JIRA Issue":
                    issue_key_stripped = issue_key.strip()
                    url = f"https://trader.atlassian.net/browse/{issue_key_stripped}"
                    jira_url_formatted = Logger.format_message(url, Logger.INFO)
                    issue_formatted = Logger.format_message(issue_key_stripped, Logger.INFO_SECONDARY)
                    Logger.log_info(f"Opening JIRA issue {issue_formatted} in browser: {jira_url_formatted}")
                    os.system(f"open {url}")

                    wait_for_enter("Waiting for confirmation before retrying...")
                    continue

    # Day-level residual reconciliation: recover any time lost to rounding so
    # the total logged for a day matches the raw total (no net loss/overage).
    for day in sorted(day_raw_totals):
        deficit = day_raw_totals[day] - day_logged_totals[day]
        if deficit <= 0:
            if deficit < 0:
                Logger.log_info(Logger.format_message(
                    f"{day}: over-reported {seconds_to_human_readable(-deficit)} due to rounding (no action taken).",
                    Logger.WARNING,
                ))
            continue

        deficit_formatted = seconds_to_human_readable(deficit)
        Logger.log_info(Logger.format_message(
            f"{day}: {deficit_formatted} lost to rounding; recovering as a residual worklog.",
            Logger.INFO,
        ))

        ticket = residual_ticket
        if not ticket:
            options = list(dict.fromkeys(day_synced_keys[day])) + ["Enter custom ticket"]
            choice = input_choice(f"Select ticket for {day} residual ({deficit_formatted})", options)
            ticket = choice if choice != "Enter custom ticket" else input("Enter ticket key: ").strip()

        try:
            with create_api_loader("Validating residual JIRA issue") as loader:
                issue_details = jira_api.get_issue_details(ticket)
                issue_id = issue_details["id"]
                issue_summary = issue_details.get("fields", {}).get("summary", "")

            with create_api_loader("Syncing residual to Tempo") as loader:
                jira_tempo_api.add_worklog(
                    issue_id=issue_id,
                    time_spent_seconds=deficit,
                    start_date=day,
                    description="Rounding residual",
                )
            Logger.log_info(Logger.format_message(
                f"{day}: residual {deficit_formatted} logged to {ticket} ({issue_summary}).",
                Logger.INFO,
            ))
        except Exception as e:
            error_message = e.response.text if isinstance(e, requests.exceptions.HTTPError) else str(e)
            Logger.log_error(Logger.format_message(
                f"{day}: failed to log residual to {ticket}: {error_message}",
                Logger.ERROR,
            ))

    # Print enhanced summary
    progress.print_summary()



def get_past_working_day() -> str:
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    while yesterday.weekday() in [5, 6]:
        yesterday -= datetime.timedelta(days=1)

    return yesterday.strftime("%Y-%m-%d")


def print_help():
    help_cmd = Logger.format_message("python cli.py sync [start_date] [end_date] [--round-seconds N] [--residual-ticket KEY]", Logger.INFO_SECONDARY)
    Logger.log_info(f"Usage: {help_cmd}")
    Logger.log_info("start_date and end_date are optional. If not provided, the script will prompt for them.")
    Logger.log_info("--round-seconds: round each entry's duration to this many seconds (default: 60). Larger windows (e.g. 1800 for 30 min) can lose time, recovered via a residual worklog.")
    Logger.log_info("--residual-ticket: JIRA issue key to receive rounding residual worklogs, skipping the interactive prompt.")


def main(*args, round_seconds: int = 60, residual_ticket: Optional[str] = None):
    start_date, end_date = None, None

    if len(args) > 0 and args[0] == "help":
        print_help()
        return

    if len(args) > 0:
        start_date = args[0]

    if len(args) == 2:
        end_date = args[1]

    last_working_day = get_past_working_day()

    if not start_date:
        default_date = Logger.format_message(last_working_day, Logger.INFO_SECONDARY)
        start_date = input(f"Enter start date (yyyy-mm-dd) [{default_date}]: ") or last_working_day

    if not end_date:
        default_date = Logger.format_message(last_working_day, Logger.INFO_SECONDARY)
        end_date = input(f"Enter end date (yyyy-mm-dd) [{default_date}]: ") or last_working_day

    sync(start_date, end_date, round_seconds=round_seconds, residual_ticket=residual_ticket)
