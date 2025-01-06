import os
import datetime

import requests
from toggle_api import TogglTrackAPI
from jira_tempo_api import JiraTempoAPI
from pprint import pprint
from config import config


TOGGL_TRACK_AUTH_TOKEN = config.toggl.api_key
JIRA_TEMPO_AUTH_TOKEN = config.tempo.api_key
JIRA_TEMPO_ACCOUNT_ID = config.tempo.user_id


def confirm(message: str):
    print(message)

    print("Confirm? [y/n]: ", end="")
    return input(f"{message} [y/n]: ").lower().strip() == "y"

def input_choice(prompt: str, choices: list):
    print(prompt)
    for i, choice in enumerate(choices):
        print(f"{i+1}. {choice}")

    choice = input(f"Enter choice [1-{len(choices)}]: ")
    try:
        return choices[int(choice)-1]
    except (ValueError, IndexError, KeyError):
        print("Invalid choice. Please try again.")
        return input_choice(prompt, choices)

def wait_for_enter(msg: str):
    input(f"{msg}. Press enter to continue...")

def seconds_to_human_readable(seconds: int):
    return str(datetime.timedelta(seconds=seconds))

def input_or_default(prompt: str, default: str):
    value = input(f"{prompt} [{default}]: ")
    return value or default

def sync(start_date: str, end_date: str = None):
    toggl_api = TogglTrackAPI(auth_token=TOGGL_TRACK_AUTH_TOKEN)
    jira_tempo_api = JiraTempoAPI(account_id=JIRA_TEMPO_ACCOUNT_ID, auth_token=JIRA_TEMPO_AUTH_TOKEN)

    entries = toggl_api.get_time_entries(
        start_date=start_date,
        end_date=end_date,
        group=True,
        round_seconds_to=60,
        skip_entry_substr="SKIP",
        exclude_tags=["banked_hours"],
        exclude_projects=["Hours Bank"],
    )

    for entry in entries:
        issue_key = entry["description"].split(":")[0]
        issue_description = "--" in entry["description"] and entry["description"].split("--")[1] or ""
        issue_description = issue_description.strip()
        duration = entry["duration"]
        datetime_obj = datetime.datetime.strptime(entry["start"], "%Y-%m-%dT%H:%M:%S+00:00")
        start_date = datetime_obj.date()

        while True:
            try:
                print(f"Adding worklog for {issue_key} with {seconds_to_human_readable(duration)} on date {start_date} with description \"{issue_description}\".")

                jira_tempo_api.add_worklog(
                    issue_key=issue_key,
                    time_spent_seconds=duration,
                    start_date=str(start_date),
                    description=issue_description
                )
                break

            except Exception as e:
                if isinstance(e, requests.exceptions.HTTPError):
                    try:
                        error_message = e.response.json()
                    except:
                        error_message = e.response.text
                else:
                    error_message = str(e)

                print(f"Failed to add worklog for {issue_key}: {error_message}")

                choice = input_choice("Choose an option:", ["Retry", "Skip", "Manual Entry", "Open JIRA Issue", "Exit"])

                if choice == "Retry":
                    print("Retrying...")
                    continue

                elif choice == "Skip":
                    print("Skipping...")
                    break

                elif choice == "Exit":
                    exit(1)

                elif choice == "Manual Entry":
                    issue_key = input_or_default("Issue key", issue_key)
                    duration = int(input_or_default("Time spent (seconds)", str(duration)))
                    start_date = input_or_default("Start date (YYYY-MM-DD)", str(start_date))
                    issue_description = input_or_default("Description", issue_description)
                    continue

                elif choice == "Open JIRA Issue":
                    url = f"https://trader.atlassian.net/browse/{issue_key.strip()}"
                    os.system(f"open {url}")

                    wait_for_enter("Waiting for confirmation before retrying...")
                    continue



def get_past_working_day() -> str:
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    while yesterday.weekday() in [5, 6]:
        yesterday -= datetime.timedelta(days=1)

    return yesterday.strftime("%Y-%m-%d")


def print_help():
    print("Usage: python cli.py sync [start_date] [end_date]")
    print("start_date and end_date are optional. If not provided, the script will prompt for them.")


def main(*args):
    start_date, end_date = None, None

    if len(args) > 0 and args[0] == "help":
        print_help()
        return

    if len(args) > 0:
        start_date = args[0]

    if len(args) == 2:
        end_date = args[1]

    if not start_date:
        last_working_day = get_past_working_day()

        start_date = input(f"Enter start date (yyyy-mm-dd) [{last_working_day}]: ") or last_working_day

    if not end_date:
        end_date = input(f"Enter end date (yyyy-mm-dd) [{last_working_day}]: ") or last_working_day

    sync(start_date, end_date)
