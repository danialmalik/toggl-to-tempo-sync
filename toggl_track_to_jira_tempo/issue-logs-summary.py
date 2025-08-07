import requests
import sys
from config import config
from collections import defaultdict
from colorama import Fore, Style, init

from jira_api import JiraAPI
from jira_tempo_api import JiraTempoAPI

# Initialize colorama for cross-platform support
init(autoreset=True)


def get_time_entries(issue_key, filter_user=None):
    """ Fetch and filter time entries logged against an issue. """
    api = JiraTempoAPI(config.tempo.user_id, config.tempo.api_key)
    jira_api = JiraAPI(config.jira.subdomain, config.jira.user_email, config.jira.api_token)
    issue_id = jira_api.get_issue_details(issue_key)["id"]
    entries = api.get_worklogs_for_issue(issue_id)

    user_logs = defaultdict(float)
    total_logged = 0

    for entry in entries:
        user_data = jira_api.get_user_details(entry["author"]["accountId"])
        user_name = user_data["displayName"]
        time_spent_hours = entry["timeSpentSeconds"] / 3600

        if filter_user and user_name.lower() != filter_user.lower():
            continue  # Skip entries if filtering by user

        user_logs[user_name] += time_spent_hours
        total_logged += time_spent_hours

    return total_logged, user_logs


def collect_issues(issue_key):
    """ Recursively collect all issues (Epic -> Child Issues -> Subtasks). """
    api = JiraAPI(config.jira.subdomain, config.jira.user_email, config.jira.api_token)

    issue_list = []
    queue = [(issue_key, 0)]  # (issue_key, level)

    while queue:
        current_issue, level = queue.pop(0)
        issue_type, issue_title = api.get_issue_type_and_title(current_issue)
        issue_list.append((current_issue, issue_title, level))

        sub_issues = []
        if issue_type == "Epic":
            sub_issues = api.get_epic_child_issues_summaries(current_issue)
        sub_issues.extend(api.get_sub_tasks_summaries(current_issue))

        for sub_issue in sub_issues:
            queue.append((sub_issue[0], level + 1))

    return issue_list

def process_issues(issue_list, filter_user=None):
    """ Process issues and format aligned, colored output. """
    max_key_length = max(len(issue[0]) for issue in issue_list)  # Find longest key for alignment
    max_title_length = max(len(issue[1]) for issue in issue_list)  # Find longest title for alignment
    max_hours_length = 10  # Set a fixed length for the hours column

    total_logged_hours = 0

    for issue_key, issue_title, level in issue_list:
        total_time, user_logs = get_time_entries(issue_key, filter_user)

        if total_time == 0:
            continue  # Skip issues with no logged time if filtering by user

        total_logged_hours += total_time
        indent = "  " * level
        key_padding = " " * (max_key_length - len(issue_key))  # Dynamic spacing for alignment
        title_padding = " " * (max_title_length - len(issue_title))  # Dynamic spacing for alignment

        # Apply colors to key, title, and hours
        colored_key = f"{Fore.CYAN}{issue_key}{Style.RESET_ALL}"
        colored_title = f"{Fore.YELLOW}{issue_title}{Style.RESET_ALL}"
        colored_time = f"{Fore.GREEN}{total_time:>10.2f} hours{Style.RESET_ALL}"

        print(f"{indent}- {colored_key}{key_padding} ({colored_title}){title_padding}: {colored_time}")

        for user, hours in user_logs.items():
            user_indent = "  " * (level + 1)
            colored_user = f"{Fore.LIGHTWHITE_EX}{user}{Style.RESET_ALL}"
            colored_user_hours = f"{Fore.GREEN}{hours:>10.2f} hours{Style.RESET_ALL}"
            print(f"{user_indent}  - {colored_user}: {colored_user_hours}")

    return total_logged_hours

def main(issue_key, filter_user=None):
    """ Main function to process an issue and its hierarchy. """
    try:
        print("\nTime Logged Summary:")
        print(f"{Fore.MAGENTA}{'─' * 100}{Style.RESET_ALL}")

        issue_list = collect_issues(issue_key)
        total_logged_hours = process_issues(issue_list, filter_user)

        print(f"{Fore.MAGENTA}{'─' * 100}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Total Logged Time: {total_logged_hours:>10.2f} hours{Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python script.py <ISSUE-KEY> [USER-NAME]{Style.RESET_ALL}")
        sys.exit(1)

    issue_key = sys.argv[1]
    user_name = sys.argv[2] if len(sys.argv) > 2 else None  # Optional user name filter
    main(issue_key, user_name)
