import hashlib
import json
import os
import random
import string
from contextlib import suppress
from requests.models import Response
from datetime import datetime, timedelta

from jsonschema import RefResolver, validate
import pytz

from tabulate import tabulate

from main.common.constants.constants import (
    DATE_PATTERN,
    CONTEXT_MAPPING,
    DATE_TIME_PATTERN,
)
from main.features.tools import file_tool


class SchemaRefResolver(RefResolver):
    """use to get resolver for $ref on locally stored schemas"""

    def resolve_remote(self, uri: str) -> dict:
        # check if uri points to a local file then we override resolve_local
        if os.path.isfile(uri):
            return self.resolve_local(uri)
        else:
            return super().resolve_remote(uri)

    def resolve_local(self, path: str) -> dict:
        with open(path) as file:
            schema = json.load(file)

        if self.cache_remote:
            self.store[path] = schema
        return schema


def validate_json_schema(response: Response, schema: json, resolver: dict):
    validate(response.json(), json.loads(schema), resolver=resolver)


def random_string(length=24, for_json_use=True):
    punctuation = (
        string.punctuation.replace('"', "").replace("\\", "")
        if for_json_use
        else string.punctuation
    )
    return "".join(
        random.choices(string.digits + string.ascii_letters + punctuation, k=length)
    )


def generate_string_by_alias(alias, max_length=500):
    result = as_number_if_possible(alias)
    if alias == "short_string":
        result = alias + "_" + random_string()
    if alias == "long_string":
        result = alias + "_" + random_string(max_length)
    if "count_symbols_" in alias:
        count = int(alias.split("_")[-1])
        result = "" + random_string(count)
    return result


def as_number_if_possible(number):
    # empty was added to more readable behave parametrization
    if number not in ("", None, "empty"):
        try:
            number = float(number)
            if number == int(number):
                return int(number)
            else:
                return number
        except ValueError:
            return number
    else:
        return None


def as_bool_if_possible(data):
    """will return bool if possible or number if possible or string as is"""
    result = as_number_if_possible(data)
    if isinstance(data, str):
        if data.lower() in ("no", "false"):
            result = False
        elif data.lower() in ("yes", "true"):
            result = True
    return result


def to_fixed_precision(number, precision):
    number = as_number_if_possible(number)
    if isinstance(number, (float, int)):
        return f"{number:.{precision}f}"
    else:
        return number


def generate_documenting_personnel(context, physician_choose):
    physician = physician_choose
    if physician_choose == "prescribing_physician":
        physician = context.account.physician["id"]
    elif physician_choose == "other_physician":
        # todo: find the way get physicians
        physician = 131074  # hardcoded Michaela Quinn
    elif physician_choose == "invalid_physician":
        physician = context.account.physician["id"] + random.randint(100, 200)
    elif physician_choose == "empty":
        physician = None
    return physician


def get_formatted_date_by_alias(
    context, date_alias: str, pattern: str = DATE_PATTERN
) -> str:
    """Allow us to use some human-readable parametrisation etc"""
    base = {
        "empty": None,
        "Today": datetime.now().strftime(pattern),
        "Yesterday": (datetime.now() - timedelta(days=1)).strftime(pattern),
        "Tomorrow": (datetime.now() + timedelta(days=1)).strftime(pattern),
        "After week": (datetime.now() + timedelta(weeks=1)).strftime(pattern),
        "After month": (datetime.now() + timedelta(weeks=4)).strftime(pattern),
        "created_date": context.created_date
        if hasattr(context, "created_date")
        else datetime.now().strftime(pattern),
        "received_time": context.received_time
        if hasattr(context, "received_time")
        else datetime.now().strftime(pattern),
    }
    if "plus" in date_alias:
        alias, delta = date_alias.split("plus")
        delta = {x[1]: int(x[0]) for x in [delta.lstrip().split()]}
        return (
            datetime.strptime(base.get(alias.strip()), pattern) + timedelta(**delta)
        ).strftime(pattern)
    elif "minus" in date_alias:
        alias, delta = date_alias.split("minus")
        delta = {x[1]: int(x[0]) for x in [delta.lstrip().split()]}
        return (
            datetime.strptime(base.get(alias.strip()), pattern) - timedelta(**delta)
        ).strftime(pattern)
    else:
        return base.get(date_alias)


class ApiList(list):
    """sortable, pretty printable list can be extended with list of model classes"""

    def __init__(self, source_list=None):
        """source_list is a list containing any objects"""
        if source_list:
            super(ApiList, self).__init__(source_list)
        else:
            super(ApiList, self).__init__()

    def __repr__(self):
        return tabulate(
            [[v for k, v in x.__dict__.items()] for x in self],
            headers=list(
                filter(lambda n: not n.startswith("_"), super().__dict__.keys())
            ),
            tablefmt="pipe",
        )

    def get_random_one(self):
        return random.choice(self)

    def get_random_few(self, count=2):
        return random.choices(self, k=count)

    def sort_by(self, attr_name, reverse=False):
        self.sort(key=lambda x: getattr(x, attr_name), reverse=reverse)

    def filter_by(self, **kwargs):
        """return new instance of Api list with objects that passed a filtration"""
        result = self
        for name, value in kwargs.items():
            if isinstance(value, list):
                result = filter(lambda x: getattr(x, name) in value, result)
            else:
                result = filter(lambda x: getattr(x, name) == value, result)
        return ApiList(result)

    def filter_by_not_in(self, **kwargs):
        """return new instance of Api list with objects that passed a filtration"""
        result = self
        for name, value in kwargs.items():
            if isinstance(value, list):
                result = filter(lambda x: getattr(x, name) not in value, result)
            else:
                result = filter(lambda x: getattr(x, name) != value, result)
        return ApiList(result)


def convert_datetime_string_to_pattern(
    string_to_convert: str,
    pattern_to_read: str,
    pattern_to_convert: str,
    as_utc: bool = False,
):
    date = datetime.strptime(string_to_convert, pattern_to_read)
    if as_utc:
        date = datetime.utcfromtimestamp(date.timestamp())
    return date.strftime(pattern_to_convert)


def get_value_from_context_accounts(context, position, key):
    """"""
    if hasattr(context, "accounts") and position in context.accounts:
        return getattr(context.accounts.get(position), key)
    else:
        raise ValueError(f"There is no accounts list or position {position} in list")


def get_dict_value_by_list_of_keys(initial_dict: dict, list_of_keys: list = None):
    if not list_of_keys:
        return initial_dict
    if list_of_keys[0] in initial_dict:
        step = initial_dict.get(list_of_keys.pop(0))
    else:
        raise ValueError(
            f"End of iteration: There is no key {list_of_keys[0]} in dict {initial_dict}"
        )
    return get_dict_value_by_list_of_keys(step, list_of_keys) if list_of_keys else step


def get_appropriate_value_from_context_by_alias(
    context, name_of_context_key, value_alias
):
    """Try to get real value from context by alias of context key
    name_of_context_key: param: 'patient' -> will try to get patient id from context or accounts depands on value
    value_alias: param: 'first' or 'second' will try to get from context.accounts, current directly from context"""
    value = None
    mapping = CONTEXT_MAPPING.get(name_of_context_key).split(".")
    if "current" in value_alias:
        value = getattr(context, mapping.pop(0))
    elif "first" in value_alias:
        value = get_value_from_context_accounts(context, "first", mapping.pop(0))
    elif "second" in value_alias:
        value = get_value_from_context_accounts(context, "second", mapping.pop(0))
    return get_dict_value_by_list_of_keys(value, mapping) if value else None


def get_date_pattern_by_alias(date_alias):
    if any([x in date_alias for x in ("start", "discontinue", "resolved")]):
        return DATE_PATTERN
    else:
        return DATE_TIME_PATTERN


def generate_params_from_parametrization(context, raw_parametrization):
    """raw_parametrization: "patient: first, document_date__lte: Today"
    return:  params dict like {'patient': 140762282328065, 'document_date__lte': "2022-05-17T13:30:49Z"}"""
    params = {}
    date = None
    base = raw_parametrization.split(",")
    for element in base:
        key, value = element.split(":")
        # here we clear the rows from whitespaces to avoid typos in parametrization
        value = value.strip()
        key = key.strip()
        # here we get all we need from context by keywords
        if key in ("patient", "prescribing_physician", "practice", "practice_created"):
            # For some reason we use practice_created instead practice in handout endpoint
            context_key = "practice" if key == "practice_created" else key
            value = get_appropriate_value_from_context_by_alias(
                context, context_key, value
            )
        if any([x in key for x in ["date", "time"]]):
            # check if value is date keyword
            pattern = get_date_pattern_by_alias(key)
            date = get_formatted_date_by_alias(context, value, pattern)
        # Check if value is bool keyword else will return number if possible or string as is
        params[key] = date or as_bool_if_possible(value)
        if "content" == key:
            params[key] = file_tool.TEST_FILES.get(value)
        if "tags" == key:
            params[key] = value.split(";")
    return params


def remove_api_filter_key_word(parameter: str) -> str:
    """get rid from filter part as __gte, __lte etc"""
    if "__" in parameter:
        return parameter[: parameter.find("__")]
    else:
        return parameter


def check_equality(key: str, value: any, possible_params: dict) -> bool:
    """We can check if some real value is suitable according to the filters
    :param key: reals node name from response
    :param value: real node value from response
    :param possible_params: dict with  filters, like
    {"document_date__gte": "2022-05-18T10:03:03Z", "document_date__gte": "2022-05-18T15:00:00Z"}
    :return: True if value is suitable according to all applicable filters
    """
    result_ = []
    # get rid from filter part as __gte, __lte etc
    params = {remove_api_filter_key_word(x): y for x, y in possible_params.items()}
    if not params.get(key):
        return False
    # if date then apply datetime matching for actual date vs filters dates as real value is a string
    elif any([x in key for x in ["date", "time"]]):
        # iteration is here for handling case when filters are the interval between two dates  __gte and __lte
        for filter_key, filter_value in possible_params.items():
            # filter object can store not suitable keys for datetime converting like practice etc., so we check
            if key in filter_key:
                pattern = get_date_pattern_by_alias(filter_key)
                actual_data, filter_data = [
                    datetime.strptime(x, pattern) for x in (value, filter_value)
                ]
                result_.append(
                    actual_data >= filter_data
                    if "__gte" in filter_key
                    else actual_data <= filter_data
                )
    else:
        if isinstance(value, list):
            result_.append(params.get(key) in value)
        else:
            result_.append(value == params.get(key))
    return all(result_)


def apply_filter_to_response(full_response_list: list, **filters: dict) -> list:
    """here we use list of object from real response and dict with filter
    we want to apply in the result list  will be added object that passed the filtration"""
    filter_result = []
    # remove __gte __lte part to keep len equal with real response
    # for case when more and less is applied simultaneously for the same node
    params = {remove_api_filter_key_word(x): y for x, y in filters.items()}
    # here we are going to match each response object with filters
    for step in full_response_list:
        # here we find all nodes that correspond to the filters
        step_dict = {x: y for x, y in step.items() if check_equality(x, y, filters)}
        # if len matched node dict the same, then object from real response is fully correspond to the filters
        if len(step_dict) == len(params):
            # then we create a list of  object that passed filtration
            filter_result.append(step)
    return filter_result


def simplify_tag_object(response_json: dict, fields_to_leave: list):
    for tag in response_json["tags"]:
        [tag.pop(x, None) for x in tag.copy() if x not in fields_to_leave]


def remove_keys_in_nested_dict(initial_dict: dict, key_to_remove: list):
    """Use for case where we need to get-rid of some keys which we can't predict
    or any other cases where we need to remove keys regardless of how deeply it nested"""
    if not key_to_remove or not isinstance(initial_dict, dict):
        return
    for key in key_to_remove:
        with suppress(KeyError):
            del initial_dict[key]
    for value in initial_dict.values():
        if isinstance(value, dict):
            remove_keys_in_nested_dict(value, key_to_remove)
        if isinstance(value, list):
            for nested in value:
                remove_keys_in_nested_dict(nested, key_to_remove)


def convert_local_datetime_to_utc(
    local_time: str,
    local_timezone: str,
    pattern_to_read: str,
    pattern_to_convert: str = None,
):
    """Use pattern_to_convert
    if we need convert to another pattern simultaneously with converting in utc"""
    initial_time = datetime.strptime(local_time, pattern_to_read)
    if initial_time.tzinfo:
        utc_time = initial_time.astimezone(pytz.utc)
    else:
        utc_time = (
            pytz.timezone(local_timezone).localize(initial_time).astimezone(pytz.utc)
        )
    return utc_time.strftime(pattern_to_convert or pattern_to_read)


def get_content_sha256(content):
    if content:
        sha256 = hashlib.sha256()
        sha256.update(content)
        return sha256.hexdigest()
    return


# Please do not remove this commented func. it can be useful in future
#  when we need to re-generate png file representation if Pillow version changes on the dev
# def convert_to_png(local_path: str,
#                    width: int = None,
#                    height: int = None,
#                    file_name: str = None) -> None:
#    """Use this func to convert original images to png in patient photo feature
#     to update parametrization files with correct data if dev pillow version changes"""
#     # install Pillow same version as dev (for now 31.08.2022 it's Pillow~=8.3.2)
#     from PIL import Image, ImageOps
#     # Please note, output file size strongly depends on Pillow (PIL) lib version
#     # Currently on the dev we use 8.3.2 to keep tests on the same page with dev use same version
#     img = Image.open(local_path)
#     if width and height:
#         # apply crop to fit
#         img = ImageOps.fit(
#             img, (int(width), int(height)), Image.ANTIALIAS, 0, (0.5, 0.5)
#         )
#     if img.mode not in ("RGB", "RGBA", "1", "P"):
#         img = img.convert("RGB")
#     # save to temp directory
#     img.save(f"tmp/{file_name.replace('.', '_')}.png")
#     img.close()


