import json
from pkg_resources import resource_string

from main.common.constants.schema_map import RESOURCES_JSON_SCHEMAS


def get_properties_from_json_schema(file_schema: str, required_only: bool = False):
    schema = json.loads(resource_string(RESOURCES_JSON_SCHEMAS, file_schema))
    if required_only:
        return schema.get("required")
    else:
        return list(schema.get("properties").keys())


def get_status_code(response):
    return response.status_code


def get_pretty_json(str_json):
    parsed = json.loads(str_json)
    return json.dumps(parsed, sort_keys=False, indent=2, separators=(",", ": "))


def is_json(str_json):
    try:
        json.loads(str_json)
    except ValueError:
        return False
    return True


def print_response(response):
    line = (
        "\n"
        + "*" * 90
        + " \nURI: "
        + response.url
        + " \nStatus code: "
        + str(get_status_code(response))
        + " \n"
        + "*" * 90
    )
    content = response.text
    if is_json(content):
        print(line + "\n" + get_pretty_json(content))
    else:
        print(line + "\n" + content)

