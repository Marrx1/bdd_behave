import logging

from behave.fixture import use_fixture_by_tag
from behave.model_core import Status

from main.common.matchers.common_matchers import contains_common_error_message
from main.features.fixtures import get_user_account_fixture


fixtures_by_tag = {
    "fixture.get_user_account": get_user_account_fixture
}


def before_all(context):
    context.config.setup_logging()
    context.fixture_log = logging.getLogger("fixture")
    context.api_error_matcher = contains_common_error_message


def after_step(_context, step):
    if step.status == Status.failed:
        if hasattr(step, "exception") and hasattr(step.exception, "response"):
            print(step.exception.response.content)


def before_tag(context, tag):
    if tag and tag.startswith("fixture."):
        context.fixture_log.info("Applying fixture: {fixture}".format(fixture=tag))
        use_fixture_by_tag(tag, context, fixtures_by_tag)

