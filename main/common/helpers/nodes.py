import pprint
import dpath.util
from six import string_types
from requests.models import Response
from main.common.helpers.api_helpers import is_json, print_response
from main.common.helpers.common_helpers import as_number_if_possible


def get_node_value(item, glob):
    """glob = 'a/b/c/0'"""
    return list(dpath.util.search(item, glob, yielded=True))[0][1]


def get_node(resp, glob, node_title):
    """glob = 'a/b/c/0'"""
    try:
        node = get_node_value(resp.json(), glob.replace("//", "/"))
        if isinstance(node, string_types) and node.isdigit():
            return as_number_if_possible(node)
        else:
            return node
    except Exception as ex:
        print_response(resp)
        raise ValueError(
            f"""Error: node '{node_title}' is not extracted: {ex}
                             URI: {resp.url}
                             Status code: {resp.status_code}
                             {pprint.pformat(resp.json()) if is_json(resp.text) else resp.text}
                          """
        )


def get_nodes(response, func_single_node):
    if get_results(response) is None:
        print_response(response)
        raise TypeError("Error: data node is empty")
    length = len(get_results(response))
    lst_ = []
    for i in range(length):
        n = func_single_node(response, str(i))
        lst_.append(n)
    return lst_


def get_id(response, index=0):
    return get_node(response, f"results/{index}/id", "id")


def get_ids(response):
    return get_nodes(response, get_id)


def get_common_error_message(response, index=0):
    """Use this to find and return a message in case error by some field
    like:{"medication":["This field may not be null."]}"""
    return get_node(response, f"*/{index}", "error message")


def get_medication_entity_error_message(response, index=0):
    """Use this to find and return a message in case error by some field
    like:{"medication":{"ndc": ["This field may not be null."]}}"""
    return get_node(response, f"medication/*/{index}", "medication error message")


def get_content_error_message(response, index=0):
    """Use this to find and return a message in case error by some field
    like:{"medication":{"ndc": ["This field may not be null."]}}"""
    return get_node(response, f"content/*/{index}", "medication error message")


def get_node_is_absent_error_message(response, index=0):
    """Use this to find and return a message in case error where there is no required node
    ["some error text"]"""
    return get_node(response, f"{index}", "error message")


def get_medication_id(response):
    # use for ui items list where we have list as root object
    return get_node(response, "0/id", "id")


def get_medication_matches(response):
    return get_node(response, "matches", "medication_matches_list")


def get_results(response):
    return get_node(response, "results", "get results")


def get_deleted_date(response: Response):
    return get_node(response, "deleted_date", "deleted date")


def get_raw_text_error_message(response):
    return response.content.decode("utf-8")


def get_node_raw_text_error_message(response):
    return get_node(response, "*", "node error text")
