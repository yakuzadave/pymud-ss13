Feature: TUI Game Commands
  As a logged-in player
  I want to execute game commands through the TUI
  So that I can interact with the game world

  Background:
    Given I am logged into the TUI as "testuser"
    And I am on the game screen

  Scenario: Execute look command
    When I type "look" and press Enter
    Then I should see the current location description
    And I should see a list of visible items
    And I should see a list of other characters

  Scenario: View command history
    Given I have typed "look" and pressed Enter
    And I have typed "inventory" and pressed Enter
    When I press the Up arrow key
    Then the input should show "inventory"
    When I press the Up arrow key again
    Then the input should show "look"

  Scenario: Clear input with Escape
    Given I have typed "some command text"
    When I press the Escape key
    Then the input field should be empty

  Scenario: Clear log with Ctrl+L
    Given the terminal log has multiple messages
    When I press Ctrl+L
    Then the terminal log should be cleared
    And I should see "Log cleared." message

  Scenario: Color-coded message types
    When the server sends an error message
    Then I should see the message in red with ❌ icon
    When the server sends a system message
    Then I should see the message in yellow with ℹ️ icon
    When the server sends a broadcast
    Then I should see the message in magenta with 📢 icon
    When the server sends a success message
    Then I should see the message in green with ✅ icon

  Scenario: Execute movement command
    When I type "north" and press Enter
    Then I should see "You move north"
    And the location name should update
    And the location description should update

  Scenario: Execute invalid command
    When I type "invalidcommand123" and press Enter
    Then I should see "Unknown command" in red
    Or I should see command suggestions
