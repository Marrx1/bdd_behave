from typing import Callable
from hamcrest.core.base_matcher import BaseMatcher
from six import string_types
from main.common.helpers.api_helpers import get_status_code, print_response
from main.common.helpers.nodes import (
    get_common_error_message,
    get_medication_id,
    get_medication_entity_error_message,
    get_node_is_absent_error_message,
    get_node,
    get_results,
    get_ids,
    get_content_error_message,
    get_deleted_date,
    get_raw_text_error_message,
    get_node_raw_text_error_message,
)


class HasStatusCode(BaseMatcher):
    def __init__(self, status):
        self.status = status

    def _matches(self, item):
        return get_status_code(item) == self.status

    def describe_to(self, description):
        description.append_text("status code should be ").append_text(str(self.status))

    def describe_mismatch(self, item, mismatch_description):
        print_response(item)
        mismatch_description.append_text("\n     actual was ").append_text(
            str(get_status_code(item))
        )


def has_status_code(status):
    return HasStatusCode(status)


class ContainsNode(BaseMatcher):
    """Check if response node value is equal to expected"""

    def __init__(self, value, func, title, node=None):
        self.value = value
        self.func = func
        self.title = title
        self.obj = None

    def _matches(self, item):
        self.obj = self.func(item)
        if self.value in [None, 0, ""]:
            return self.func(item) in [None, 0, ""]
        else:
            _type = type(self.value)
            try:
                if isinstance(self.value, string_types):
                    self.obj = (
                        self.obj if isinstance(self.obj, string_types) else self.obj
                    )
                else:
                    self.obj = self.func(item)
                return _type(self.obj) == self.value
            except TypeError:
                print_response(item)
                raise ValueError("Value must be number")

    def describe_to(self, description):
        description.append_text(f'{self.title} should be "{self.value}"')

    def describe_mismatch(self, item, mismatch_description):
        print_response(item)
        mismatch_description.append_text(f'\n     actual was "{self.obj}"')


def contains_common_error_message(value):
    return ContainsNode(value, get_common_error_message, "error message")


def contains_medication_object_error(value):
    return ContainsNode(value, get_medication_entity_error_message, "error message")


def contains_node_is_absent_error(value):
    return ContainsNode(value, get_node_is_absent_error_message, "error message")


def contains_ui_medication_id(value):
    return ContainsNode(value, get_medication_id, "medication_id")


def contains_base64_content_is_absent_error(value):
    return ContainsNode(value, get_content_error_message, "error message")


def contains_raw_text_error_message(value):
    return ContainsNode(value, get_raw_text_error_message, "error_message")


def contains_node_raw_text_error_message(value):
    return ContainsNode(value, get_node_raw_text_error_message, "error_message")


class DoesNotContainNodes(BaseMatcher):
    def __init__(self, func, title, *values):
        self.values = list(values)
        self.func = func
        self.title = title

    def _matches(self, item):
        return all([value not in self.func(item) for value in self.values])

    def describe_to(self, description):
        description.append_text(
            f"{self.title} should not contain {sorted(self.values)}"
        )

    def describe_mismatch(self, item, mismatch_description):
        print_response(item)
        mismatch_description.append_text(f"\n     actual was {self.func(item)}")


def does_not_contains_item_with_id(*value):
    return DoesNotContainNodes(get_ids, "ids", *value)


class ContainsNotEmptyNode(BaseMatcher):
    """Check if response node value is not empty"""

    def __init__(self, func: Callable, title: str):
        self.func = func
        self.title = title
        self.obj = None

    def _matches(self, item):
        self.obj = self.func(item)
        return bool(self.obj)

    def describe_to(self, description):
        description.append_text(f"{self.title} should not be empty")

    def describe_mismatch(self, item, mismatch_description):
        print_response(item)
        mismatch_description.append_text(
            f'\n     actual {self.title}  was "{self.obj}"'
        )


def contains_not_empty_deleted_date():
    return ContainsNotEmptyNode(get_deleted_date, "deleted_date")


def contains_particular_error(value, path="*/{index}/*/{index}"):
    """Use this to find and return a message in specific case error with providing error path
    i.e. for {"cpts":[{"units":["A valid number is required."]}]} use path like */{index}/*/{index}"""
    return ContainsNode(
        value,
        lambda response, index=0: get_node(
            response, path.format(index=index), "error message"
        ),
        "error message",
    )
