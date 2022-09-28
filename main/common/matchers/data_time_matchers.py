from datetime import datetime, timedelta
from operator import sub

from hamcrest.core.base_matcher import BaseMatcher

from main.common.constants.constants import DATE_TIME_PATTERN, DATE_PATTERN


class MatchesDateTimePattern(BaseMatcher):
    """Check if string value has appropriate date or date time format according to the given pattern"""

    def __init__(self, value):
        self.value = value

    def _matches(self, item):
        # noinspection PyBroadException
        try:
            datetime.strptime(item, self.value)
        except Exception:
            return False
        else:
            return True

    def describe_to(self, description):
        description.append_text(f"Date should has format: {self.value}")

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(
            f"Actual value was {item} that not corresponded to pattern {self.value}"
        )


def matches_datetime_pattern(value):
    return MatchesDateTimePattern(value)


class ContainsCloseToTime(BaseMatcher):
    def __init__(self, value, pattern, title, error_tolerance):
        self.value = value
        self.pattern = pattern
        self.title = title
        self.error_tolerance = error_tolerance
        self.data_error = None

    def _matches(self, item):
        # case where both values are None
        if not all([item, self.value]):
            return True
        # check case where one of values is not datetime
        try:
            values = sorted(
                [datetime.strptime(x, self.pattern) for x in (item, self.value)],
                reverse=True,
            )
        except ValueError as err:
            self.data_error = f"""Incorrect format one of values\n, 
            Actual was: {item}, Expected was: {self.value}, Pattern was: {self.pattern}\n{err}"""
            return False
        except TypeError as err:
            self.data_error = f"""Incorrect type one of values\n, 
                        Actual was: {item}, Expected was: {self.value}, Pattern was: {self.pattern}\n{err}"""
            return False
        else:
            return sub(*values) <= timedelta(**self.error_tolerance)

    def describe_to(self, description):
        description.append_text(
            f"{self.title} should be {self.value} within {self.error_tolerance}"
        )

    def describe_mismatch(self, item, mismatch_description):
        if self.data_error:
            mismatch_description.append_text(self.data_error)
        else:
            mismatch_description.append_text(f"\n     Actual was {item}")


def contains_datetime_close_to(
    value: str, pattern: str = DATE_PATTERN, title: str = "datetime", **error_tolerance
):
    """error_tolerance can be one of allowable values from timedelta
    days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0"""
    if not error_tolerance:
        error_tolerance = {"seconds": 1}
    return ContainsCloseToTime(value, pattern, title, error_tolerance)
