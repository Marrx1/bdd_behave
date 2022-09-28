@fixture.get_user_account

Feature: User Profile

  # Simple test
  @smoke
  Scenario: POST profile photo via UI
    Given we have a logged in qwiki user
    When we post new user profile photo test_profile_image.jpeg
    Then we check if user profile photo is correctly posted

 # test with outline parametrization
  Scenario Outline: POST profile photo via UI
    Given we have a logged in qwiki user
    When we post new user profile photo <file_name>
    Then we check if user profile photo is correctly posted

    Examples: Profile Photo
      |file_name              |
      |test_profile_image.jpeg|
      |test_profile_image.jp2 |
      |test_profile_image.ico |
      |test_profile_image.pbm |
      |test_profile_image.pgm |
      |test_profile_image.png |

 # test with table data
  Scenario: Previously opened page is presented in the Recently viewed list
    Given we have a logged in qwiki user
    When we open scope of pages in random order
    | page_name    |
    | contact_info |
    | python       |
    | java         |
    And we get the list of Recently viewed pages
    Then we check if opened pages is in the Recently viewed list