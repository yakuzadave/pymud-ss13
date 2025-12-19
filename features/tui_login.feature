Feature: TUI Login Flow
  As a player
  I want to log into the game through the TUI
  So that I can start playing

  Background:
    Given the game server is running
    And the TUI client is launched

  Scenario: Successful login with existing account
    When I enter username "testuser"
    And I enter password "testpass123"
    And I submit the login form
    Then I should see the game screen
    And I should see a welcome message
    And the status bar should show "Connected: Yes"

  Scenario: Create new account
    When I click "Create Account"
    And I enter username "newuser"
    And I enter password "newpass123"
    And I confirm password "newpass123"
    And I submit the registration form
    Then I should see the game screen
    And I should see "Account created successfully"

  Scenario: Failed login with invalid credentials
    When I enter username "invaliduser"
    And I enter password "wrongpass"
    And I submit the login form
    Then I should see "Invalid credentials" error
    And I should remain on the login screen

  Scenario: Handle network connection error
    Given the game server is stopped
    When I try to connect
    Then I should see "Connection failed" error
    And I should see connection retry options
