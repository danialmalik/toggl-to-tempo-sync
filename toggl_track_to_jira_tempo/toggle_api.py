import datetime
import base64
from typing import Optional
import requests
import math


from config import API_REQUESTS_TIMEOUT_SECONDS

class TogglTrackAPI:
    BASE_URL = "https://api.track.toggl.com/api"
    API_VERSION = "/v9"

    GET_ENTRIES_ENDPOINT = "/me/time_entries"
    GET_USER_PROJECTS_ENDPOINT = "/me/projects"

    def __init__(self, username="", password="", auth_token=""):
        self.username = username
        self.password = password
        self.auth_token = auth_token

        if self.username and self.password:
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {self._b64_encode(f'{self.username}:{self.password}')}",
            }
        elif self.auth_token:
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {self._b64_encode(f'{self.auth_token}:api_token')}",
            }
        else:
            raise ValueError("Auth credentials are missing.")

    @staticmethod
    def _make_absolute_url(endpoint: str) -> str:
        return f"{TogglTrackAPI.BASE_URL}{TogglTrackAPI.API_VERSION}{endpoint}"

    def _make_get_request(self, url, data=None, headers=None):
        data = data or {}
        response = requests.get(url, params=data, headers=headers or self.headers, timeout=API_REQUESTS_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()

    def _b64_encode(self, string):
        return base64.b64encode(string.encode("utf-8")).decode("utf-8")

    def get_time_entries(
        self,
        start_date: str,
        end_date: str = None,
        group: bool = False,
        round_seconds_to: int = 60,
        skip_entry_substr: str = "",
        exclude_projects: list[str]=None,
        exclude_tags: list[str]=None,
        include_tags: list[str]=None,
    ):
        only_start_date = False
        exclude_projects = exclude_projects or []

        if not end_date:
            end_date = start_date
            only_start_date = True

        # Increment end date by one day because Toggl API is inclusive and does not
        # return any entries for the end date equal to the start date.
        end_date = (
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
            + datetime.timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S+00:00")


        url = self._make_absolute_url(self.GET_ENTRIES_ENDPOINT)
        entries = self._make_get_request(
            url, data={"start_date": start_date, "end_date": end_date}
        )

        if skip_entry_substr:
            entries = [
                entry for entry in entries if skip_entry_substr not in entry["description"]
            ]

        if exclude_tags:
            entries = [
                entry for entry in entries if not any(tag in entry["tags"] for tag in exclude_tags)
            ]

        if exclude_projects:
            projects_with_ids = self.get_projects(exclude_projects)
            project_ids = [project["id"] for project in projects_with_ids]
            entries = [
                entry for entry in entries if entry["project_id"] not in project_ids
            ]

        if include_tags:
            entries = [
                entry for entry in entries if any(tag in entry["tags"] for tag in include_tags)
            ]

        if only_start_date:
            entries = [
                entry
                for entry in entries
                if datetime.datetime.strptime(
                    entry["start"], "%Y-%m-%dT%H:%M:%S+00:00"
                ).date()
                == datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            ]

        if group:
            # return grouped entries with the same description and same date
            # duration should be summed up
            grouped_entries = {}
            for entry in entries:
                description = entry["description"]
                start_date = entry["start"].split("T")[0]
                key = f"{description}--{start_date}"

                if key in grouped_entries:
                    grouped_entries[key]["duration"] += entry["duration"]
                else:
                    grouped_entries[key] = entry
            entries = list(grouped_entries.values())

        if round_seconds_to:
            for entry in entries:
                entry["duration"] = round(entry["duration"]/round_seconds_to) * round_seconds_to

        return sorted(entries, key=lambda entry: entry["id"])

    def get_projects(self, filter_names: list[str]) -> Optional[int]:
        url = self._make_absolute_url(self.GET_USER_PROJECTS_ENDPOINT)
        projects = self._make_get_request(url)

        if len(filter_names):
            projects = [
                project for project in projects if project["name"] in filter_names
            ]
        return projects

    def add_tag_to_entry(self):
        pass
