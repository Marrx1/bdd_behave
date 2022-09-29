
Feature: Sign in

  # Simple test
  @sign_in
  Scenario: User try sign in with valid credentials
    Given we have a user with valid credentials
    When we do login action with valid credentials
    Then we check if user has licensed access