import re
import random
from time import sleep


from behave.runner import Context
from lxml import etree
from requests.models import Response
from hamcrest import assert_that, is_, equal_to
from pkg_resources import resource_string

from main.clients.clients import UIClient
from main.common.constants.qwiki_page_map import pages
from main.common.constants.schema_map import RECENTLY_VIEWED_SCHEMA
from main.common.constants.test_file_map import RESOURCES_TEST_FILES
from main.common.helpers.common_assertations import check_response_code_and_schema
from main.common.helpers.common_helpers import get_content_sha256
from main.features.tools.file_tool import PROFILE_IMAGES


def post_user_profile_photo(context: Context, file_name: str) -> Response:
    data = PROFILE_IMAGES.get(file_name)
    path = f"rest/user-profile/1.0/{context.user_key}/avatar/upload"
    img_data = {"avatarDataURI":
                f"data:{data.get('content_type')};base64,{data.get('base64_content')}"}
    response = context.client.post(path, json=img_data)
    return response


def get_user_account(context: Context) -> None:
    context.client = UIClient()
    response = context.client.post("dologin.action")
    response.raise_for_status()
    page = etree.HTML(response.text)
    context.user_key = page.xpath("//meta[@name='ajs-remote-user-key']")[0].get("content")
    context.username = page.xpath("//meta[@name='ajs-current-user-fullname']")[0].get("content")
    licensed_access = page.xpath("//meta[@name='ajs-remote-user-has-licensed-access']")[0].get("content")
    context.has_licensed_access = True if licensed_access == "true" else False
    context.fixture_log.info(f"logged-in as: {context.username}")


def get_user_profile_photo(context: Context, attachment_id: int) -> Response:
    path = f"download/attachments/{attachment_id}/user-avatar"
    response = context.client.get(path)
    return response


def get_api_page(context: Context, page_id: int) -> Response:
    response = context.client.get(f"rest/api/content/{page_id}")
    response.raise_for_status()
    return response


def get_ui_page(context: Context, page_id: int) -> Response:
    params = {"pageId": page_id}
    response = context.client.get("pages/viewpage.action", params=params)
    response.raise_for_status()
    return response


def get_recently_viewed_pages(context: Context) -> Response:
    params = {"includeTrashedContent": True}
    response = context.client.get(f"rest/recentlyviewed/1.0/recent", params=params)
    response.raise_for_status()
    return response


class UserProfile:
    def __init__(self, context: Context) -> None:
        self.file_name = None
        self.profile_photo_modification_date = None
        self.profile_photo_id = None
        self._context = context

    def post_profile_photo(self, file_name: str) -> "UserProfile":
        self.file_name = file_name
        response = post_user_profile_photo(self._context, file_name)
        response.raise_for_status()
        # '{"avatarPath":"/download/attachments/135991917/user-avatar?version=6&modificationDate=1664202772433&api=v2"}'
        pattern = re.compile(r'.*attachments/(?P<attachment_id>\d*)/.*modificationDate=(?P<modificationDate>\d*).*')
        match = pattern.search(response.text)
        if match:
            self.profile_photo_id = match.group("attachment_id")
            self.profile_photo_modification_date = match.group("modificationDate")
        return self

    def get_profile_photo(self) -> Response:
        response = get_user_profile_photo(self._context, self.profile_photo_id)
        response.raise_for_status()
        return response

    def check_photo_photo_is_available_on_the_ui(self) -> None:
        response = self.get_profile_photo()
        actual_hash = get_content_sha256(response.content)
        resource = resource_string(RESOURCES_TEST_FILES, self.file_name)
        expected_hash = get_content_sha256(resource)
        assert_that(
            actual_hash,
            is_(equal_to(expected_hash)),
            f"Files are not the same, check profile photo with {self.file_name}",
        )


class UserOptions:
    def __init__(self, context: Context) -> None:
        self.actual_recently_viewed_pages = None
        self.expected_recently_viewed_pages = None
        self._context = context

    def open_list_of_pages(self, pages_list: list) -> "UserOptions":
        self.expected_recently_viewed_pages = [pages[row["page_name"]] for row in pages_list]
        random.shuffle(self.expected_recently_viewed_pages)
        [get_ui_page(self._context, page) for page in self.expected_recently_viewed_pages]
        return self

    def get_recently_viewed(self) -> "UserOptions":
        response = get_recently_viewed_pages(self._context)
        check_response_code_and_schema(response, RECENTLY_VIEWED_SCHEMA)
        self.actual_recently_viewed_pages = [x.get("id") for x in response.json()]
        return self

    def check_recently_viewed(self) -> None:
        items_to_check = self.actual_recently_viewed_pages[:len(self.expected_recently_viewed_pages)]
        items_to_check.reverse()
        assert_that(items_to_check, is_(equal_to(self.expected_recently_viewed_pages)))

