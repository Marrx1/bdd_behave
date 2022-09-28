
from behave import then, when, step
from behave.runner import Context
from main.features.tools.user_tools import UserProfile, UserOptions


@when("we post new user profile photo {file_name}")
def post_new_user_profile_photo(context: Context, file_name: str) -> None:
    context.user_profile = UserProfile(context)
    context.user_profile.post_profile_photo(file_name)


@then("we check if user profile photo is correctly posted")
def check_if_user_profile_photo_posted(context: Context) -> None:
    context.user_profile.check_photo_photo_is_available_on_the_ui()


@when("we open scope of pages in random order")
def open_pages_from_given_table(context: Context) -> None:
    context.user_options = UserOptions(context)
    context.user_options.open_list_of_pages(context.table)


@step("we get the list of Recently viewed pages")
def get_resent_pages_for_current_user(context: Context) -> None:
    context.user_options.get_recently_viewed()


@then("we check if opened pages is in the Recently viewed list")
def check_recently_viewed_pages_list(context: Context) -> None:
    context.user_options.check_recently_viewed()



