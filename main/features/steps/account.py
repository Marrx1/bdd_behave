from behave import given
from behave.runner import Context
from hamcrest import assert_that, is_


@given("we have a logged in qwiki user")
def check_if_we_have_logged_in_user_acc(context: Context) -> None:
    assert_that(context.has_licensed_access, is_(True))


