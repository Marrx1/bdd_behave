
from behave import fixture
from behave.runner import Context
from main.features.tools.user_tools import get_user_account


@fixture
def get_user_account_fixture(context: Context) -> None:
    get_user_account(context)
