import requests
from functools import lru_cache
from requests.auth import HTTPBasicAuth



class JiraAPI:

    REST_BASE_URL_TEMPLATE = "https://{subdomain}.atlassian.net/rest/api/3"

    ISSUE_DETAILS_URL_TEMPLATE = f"{REST_BASE_URL_TEMPLATE}/issue/{{issue_key}}"
    SEARCH_URL_TEMPLATE = f"{REST_BASE_URL_TEMPLATE}/search?jql={{jql}}&fields=key,summary"
    USER_URL_TEMPLATE = f"{REST_BASE_URL_TEMPLATE}/user?accountId={{account_id}}"

    def __init__(self, subdomain, user_email, api_token):
        self._subdomain = subdomain

        self._auth = HTTPBasicAuth(user_email, api_token)
        self._headers = {
            "Accept": "application/json",
        }

    def _make_get_request(self, url, params=None):
        params = params or {}
        response = requests.get(url, headers=self._headers, auth=self._auth, params=params)
        response.raise_for_status()
        return response.json()

    @lru_cache(maxsize=128)
    def get_user_details(self, account_id: str) -> dict:
        url = self.USER_URL_TEMPLATE.format(
            subdomain=self._subdomain,
            account_id=account_id
        )

        return self._make_get_request(url)

    def get_issue_details(self, issue_key: str) -> dict:
        url = self.ISSUE_DETAILS_URL_TEMPLATE.format(
            subdomain=self._subdomain,
            issue_key=issue_key
        )

        return self._make_get_request(url)

    def get_issue_type_and_title(self, issue_key: str) -> tuple[str, str]:
        """Fetch issue details including title and type. """
        issue_data = self.get_issue_details(issue_key)
        issue_type = issue_data["fields"]["issuetype"]["name"]
        issue_title = issue_data["fields"]["summary"]
        return issue_type, issue_title

    def get_epic_child_issues_summaries(self, epic_key: str) -> list[tuple[str, str]]:
        """Get all child issues linked to an Epic."""
        jql = f'"Epic Link"="{epic_key}"'
        url = self.SEARCH_URL_TEMPLATE.format(
            subdomain=self._subdomain,
            jql=jql
        )

        response = self._make_get_request(url)
        issues = response["issues"]
        return [(issue["key"], issue["fields"]["summary"]) for issue in issues]

    def get_sub_tasks_summaries(self, issue_key: str) -> list[tuple[str, str]]:
        """Get all sub-tasks for a given issue."""
        issue_data = self.get_issue_details(issue_key)
        return [(sub["key"], sub["fields"]["summary"]) for sub in issue_data["fields"].get("subtasks", [])]
