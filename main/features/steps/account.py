from behave import given, when, then
from behave.runner import Context
from hamcrest import assert_that, is_
from main.clients import *
from main.features.tools.user_tools import get_user_account


@given("we have a logged in qwiki user")
def check_if_we_have_logged_in_user_acc(context: Context) -> None:
    assert_that(context.has_licensed_access, is_(True))


@given("we have a user with valid credentials")
def check_env_variable_is_in_place(context: Context):
    assert_that(all([HOST, USER_PASSWORD, USER_NAME]))


@when("we do login action with valid credentials")
def do_login_action(context: Context):
    get_user_account(context)


@then("we check if user has licensed access")
def check_user_licensed(context: Context):
    context.execute_steps("given we have a logged in qwiki user")



