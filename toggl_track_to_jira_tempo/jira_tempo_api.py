from collections import defaultdict, namedtuple
import requests
from datetime import datetime

from config import API_REQUESTS_TIMEOUT_SECONDS
from utils import Logger, HoursLog
from jira_api import JiraAPI



class JiraTempoAPI:
    BASE_URL = "https://api.tempo.io"
    API_VERSION = "/4"
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
        response = requests.get(url, params=data, headers=headers, timeout=API_REQUESTS_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()

    def _make_post_request(self, url, data: dict, headers=None):
        headers = {
            **self.headers,
            **(headers or {})
        }
        response = requests.post(url, json=data, headers=headers, timeout=API_REQUESTS_TIMEOUT_SECONDS)
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


    def get_worklogs_for_user(self, user_id: str, start_date: datetime, end_date: datetime, limit: int = 1000, offset: int = 0):
        url = f"{self.BASE_URL}{self.API_VERSION}{self.WORKLOGS_ENDPOINT}/user/{user_id}"

        data = {
            "from": start_date.strftime('%Y-%m-%d'),
            "to": end_date.strftime('%Y-%m-%d'),
            "limit": limit,
            "offset": offset
        }

        entries = []

        while True:
            response = self._make_get_request(url, data=data)
            for log in response.get("results", []):
                logged_time = log["timeSpentSeconds"] / 3600
                start_date = datetime.strptime(log["startDate"], "%Y-%m-%d").date()

                entries.append(HoursLog(start_date, logged_time))

            next_api_url = response.get("metadata", {}).get("next", "")

            if next_api_url:
                offset = offset + limit
                data["offset"] = offset
            else:
                break

        return entries

    def get_worklogs_for_issue(self, issue_id: str):
        url = f"{self.BASE_URL}{self.API_VERSION}{self.WORKLOGS_ENDPOINT}?issueId={issue_id}"
        entries = self._make_get_request(url)["results"]
        return entries


    def add_worklog(self, issue_id: str, time_spent_seconds: int, start_date: str, start_time: str="", description: str=""):
        url = f"{self.BASE_URL}{self.API_VERSION}{self.WORKLOGS_ENDPOINT}"

        request_body = {
            "authorAccountId": self.account_id,
            "issueId": issue_id,
            "timeSpentSeconds": time_spent_seconds,
            "startDate": start_date,
            # "startTime": start_time,
            "description": description
        }

        return self._make_post_request(url, data=request_body)
