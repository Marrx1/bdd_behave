
from behave import fixture
from behave.runner import Context
from faker import Faker
from lxml import etree

from main.clients.clients import UIClient


@fixture
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
