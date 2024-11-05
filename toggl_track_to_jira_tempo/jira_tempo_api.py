import requests

class JiraTempoAPI:
    BASE_URL = "https://api.tempo.io/core"
    API_VERSION = "/3"
    WORKLOGS_ENDPOINT = "/worklogs"

    def __init__(self, account_id, auth_token):
        self.account_id = account_id
        self.auth_token = auth_token

    def _make_get_request(self, url, data=None, headers=None):
        data = data or {}
        headers = {
            **self.headers,
            **(headers or {})
        }
        response = requests.get(url, params=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def _make_post_request(self, url, data: dict, headers=None):
        headers = {
            **self.headers,
            **(headers or {})
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    @property
    def headers(self):
        headers = {
            # "User-Agent": "TogglTrackToJiraTempo/0.1"
        }
        if self.auth_token:
            return {
                **headers,
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"
            }
        raise ValueError("Auth token is required")

    def add_worklog(self, issue_key: str, time_spent_seconds: int, start_date: str, start_time: str="", description: str=""):
        url = f"{self.BASE_URL}{self.API_VERSION}{self.WORKLOGS_ENDPOINT}"

        request_body = {
            "authorAccountId": self.account_id,
            "issueKey": issue_key,
            "timeSpentSeconds": time_spent_seconds,
            "startDate": start_date,
            # "startTime": start_time,
            "description": description
        }

        return self._make_post_request(url, data=request_body)
