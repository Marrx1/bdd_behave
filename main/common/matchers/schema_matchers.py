from hamcrest.core.base_matcher import BaseMatcher
from pkg_resources import resource_string

from main.common.constants.schema_map import RESOURCES_JSON_SCHEMAS
from main.common.helpers.api_helpers import print_response
from main.common.helpers.common_helpers import validate_json_schema, SchemaRefResolver


class MatchesJsonSchema(BaseMatcher):
    def __init__(self, file_schema):
        self.file_schema = file_schema
        self.ex = None

    def _matches(self, item):
        try:
            schema = resource_string(RESOURCES_JSON_SCHEMAS, self.file_schema)
            base_uri = RESOURCES_JSON_SCHEMAS.replace(".", "/") + "/"
            resolver = SchemaRefResolver(referrer=schema, base_uri=base_uri)
            validate_json_schema(item, schema, resolver)
            return True
        except Exception as ex:
            self.ex = ex
            return False

    def describe_to(self, description):
        description.append_text(
            f"response body should match json schema {self.file_schema}"
        )

    def describe_mismatch(self, item, mismatch_description):
        print("*" * 100 + f"\nJson matching error: {self.ex}")
        print_response(item)
        mismatch_description.append_text(
            f"\n     actual was:"
            f" response body did not match json schema {self.file_schema}"
            f", please see stdout"
        )


def matches_json_schema(file_schema):
    return MatchesJsonSchema(file_schema)
