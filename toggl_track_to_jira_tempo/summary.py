import calendar
import datetime
from collections import namedtuple
from typing import List, Union

import requests

from toggle_api import TogglTrackAPI
from jira_tempo_api import JiraTempoAPI, HoursLog
from config import config
from utils import Logger


TOGGL_TRACK_AUTH_TOKEN = config.toggl.api_key
JIRA_TEMPO_AUTH_TOKEN = config.tempo.api_key
JIRA_TEMPO_ACCOUNT_ID = config.tempo.user_id


def get_left_justified_string(left_string, *rest_strings, length=50, padding_char="-"):
    return left_string.ljust(length, padding_char) + "".join(rest_strings)


def get_centered_string(string, length=70, padding_char="-"):
    return string.center(length, padding_char)


def float_to_hours_minutes(value: float) -> str:
    sign = "-" if value < 0 else "+"
    return f"{sign}{int(value)}h {int((abs(value) % 1) * 60)}m"


class LogsSummary:
    hours_by_day: dict
    reference_date: datetime.date

    def __init__(self, reference_date: Union[datetime.date, None] = None) -> None:
        self.hours_by_day = {}
        self.reference_date = reference_date or datetime.datetime.today().date()

    def get_start_of_week(self, within_current_month: bool = True) -> datetime.date:
        current = self.reference_date
        last_monday = current - datetime.timedelta(days=current.weekday())
        start_of_month = datetime.date(current.year, current.month, 1)

        if within_current_month:
            return max(last_monday, start_of_month)
        else:
            return last_monday

    def add_day_hours(self, day: datetime.date, hours: float) -> None:
        self.hours_by_day[day] = self.hours_by_day.get(day, 0) + hours

    def get_total_week_hours(self, within_current_month: bool = True) -> float:
        start_date = self.get_start_of_week(within_current_month=within_current_month)

        total_hours = 0

        for day in range(start_date.weekday(), 5):
            date = start_date + datetime.timedelta(days=day)
            total_hours += self.hours_by_day.get(date, 0)

        return total_hours

    @property
    def total_month_hours(self) -> float:
        """Return total number of working hours in current month."""
        num_working_days = self.working_days_in_month
        return num_working_days * 8

    @property
    def total_month_hours_so_far(self) -> float:
        current = self.reference_date
        total_hours = 0
        for day in range(1, current.day + 1):
            date = datetime.date(current.year, current.month, day)
            total_hours += self.hours_by_day.get(date, 0)

        return total_hours

    @property
    def working_days_in_month(self) -> int:
        current = self.reference_date
        return sum(
            1 for day in range(
                1,
                calendar.monthrange(current.year, current.month)[1] + 1
            )
            if datetime.date(current.year, current.month, day).weekday() < 5
        )

    @property
    def working_days_in_month_so_far(self) -> int:
        current = self.reference_date
        working_days = 0

        for day in range(1, current.day + 1):
            date = datetime.date(current.year, current.month, day)
            if date.weekday() < 5:  # Monday to Friday (0-4 are weekdays)
                working_days += 1

        return working_days

    def get_required_hours_for_week(self, within_current_month: bool = True) -> float:
        current = self.reference_date
        if within_current_month:
            reference_week_day = min(
                # Day of the week, Monday is 0
                current.weekday() + 1,
                # Day of the month, 1-31. If the month started during the week
                # working days.
                current.day,
                # Friday. Sat and sunday are not working days.
                5,
            )
        else:
            reference_week_day = min(
                # Day of the week, Monday is 0
                current.weekday() + 1,
                # Friday (4+1). Sat and sunday are not working days.
                5,
            )

        return reference_week_day * 8

    def get_week_work_required_difference(
        self, within_current_month: bool = True
    ) -> float:
        return self.get_total_week_hours(
            within_current_month=within_current_month
        ) - self.get_required_hours_for_week(within_current_month=within_current_month)

    @property
    def required_hours_for_month(self) -> float:
        return self.working_days_in_month_so_far * 8

    @property
    def month_work_required_difference(self) -> float:
        return self.total_month_hours_so_far - self.required_hours_for_month




def get_total_hours_summary(tempos, reference_date: datetime.date) -> LogsSummary:
    logs_summary = LogsSummary(reference_date)

    week_start_date = logs_summary.get_start_of_week()
    total_hours_decimal = 0

    for tempo in tempos:
        Logger.log_debug(f"Getting hours for {tempo['name']}")
        logs_list: List[HoursLog] = get_hours(tempo, reference_date)

        current_month_total = 0
        current_week_total = 0

        for log in logs_list:
            logs_summary.add_day_hours(log.date, log.hours)
            current_month_total += log.hours

            if log.date >= week_start_date:
                current_week_total += log.hours

        Logger.log_info(
            get_left_justified_string(
                f"Logged weekly hours for {tempo['name']}",
                f": {float_to_hours_minutes(current_week_total)}",
            )
        )
        Logger.log_info(
            get_left_justified_string(
                f"Logged monthly hours for {tempo['name']}",
                f": {float_to_hours_minutes(current_month_total)}",
            )
        )
        total_hours_decimal += current_month_total

    Logger.log_info(
        get_left_justified_string(
            "Logged monthly hours decimal", f": {total_hours_decimal}"
        )
    )

    return logs_summary


def get_jira_projects() -> dict:
    return [
        {
            "name": "Project",
            "user": config.tempo.user_id,
            "tempo_token": config.tempo.api_key,
        }
    ]


def get_hours(tempo_details: dict, reference_date: datetime.date) -> List[HoursLog]:
    Logger.log_debug(f"Current Date: {reference_date}")

    first_day_month = reference_date.replace(day=1)
    Logger.log_debug(f"First day of month: {first_day_month}")

    jira_tempo_api = JiraTempoAPI(account_id=JIRA_TEMPO_ACCOUNT_ID, auth_token=JIRA_TEMPO_AUTH_TOKEN)

    return  jira_tempo_api.get_worklogs_for_user(
        user_id=tempo_details["user"],
        start_date=first_day_month,
        end_date=reference_date,
    )

def print_help():
    print("Usage: python cli.py summary [reference_date]")
    print("reference_date: YYYY-MM-DD or EOM (End of Month). Default is today.")
    return

def main(*args):
    if len(args) > 0 and args[0] == "help":
        print_help()
        return

    tempos: dict = get_jira_projects()

    reference_date = args[0] if len(args) > 0 else None

    if reference_date == "EOM":
        # Get current month's last date
        today = datetime.datetime.today()
        reference_date = today.replace(
            day=calendar.monthrange(today.year, today.month)[1]
        )
        reference_date = reference_date.strftime("%Y-%m-%d")

    if reference_date:
        try:
            Logger.log_info(f"Getting hours till {reference_date}")
            reference_date = datetime.datetime.strptime(
                reference_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            Logger.log_error(
                "Invalid reference date format. Expected YYYY-MM-DD,"
                f" got {reference_date}"
            )
            exit(1)
    else:
        Logger.log_info("Getting hours till today")
        reference_date = datetime.datetime.today().date()

    summary: LogsSummary = get_total_hours_summary(tempos, reference_date)

    Logger.log_info(
        get_centered_string("Daily Hours", padding_char="="), color=Logger.CYAN
    )
    for day, hours in summary.hours_by_day.items():
        week_day_name = calendar.day_name[day.weekday()]
        Logger.log_info(
            get_left_justified_string(
                f"{day} [{week_day_name}]", f": {float_to_hours_minutes(hours)}"
            )
        )

    Logger.log_info(
        get_centered_string("Month Hours", padding_char="="), color=Logger.CYAN
    )
    Logger.log_info(
        get_left_justified_string(
            "Total Month Hours",
            f": {float_to_hours_minutes(summary.total_month_hours)}"
        )
    )
    difference: float = summary.month_work_required_difference

    Logger.log_info(
        get_left_justified_string(
            "Logged Hours / required hours so far",
            f": {float_to_hours_minutes(summary.total_month_hours_so_far)} / ",
            f"{float_to_hours_minutes(summary.required_hours_for_month)}",
        )
    )

    color = Logger.GREEN if difference >= 0 else Logger.YELLOW

    Logger.log_info(
        get_left_justified_string(
            "Difference", f": {float_to_hours_minutes(difference)}"
        ),
        color,
    )
