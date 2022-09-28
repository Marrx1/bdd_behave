from http.client import OK
from hamcrest import assert_that, all_of

from main.common.matchers.common_matchers import has_status_code
from main.common.matchers.schema_matchers import matches_json_schema


def check_response_code_and_schema(response, schema, status_code=OK) -> None:
    assert_that(
        response,
        all_of(has_status_code(status_code), matches_json_schema(schema))
    )

