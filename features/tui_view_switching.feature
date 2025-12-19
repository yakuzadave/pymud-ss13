Feature: TUI View Switching
  As a player
  I want to switch between different TUI views
  So that I can access different game features

  Background:
    Given I am logged into the TUI as "testuser"

  Scenario: Switch to inventory view
    Given I am on the game screen
    When I press F2
    Then I should see the inventory screen
    And I should see my carried items
    And I should see my equipped items
    And I should see player stats

  Scenario: Switch to map view
    Given I am on the game screen
    When I press F3
    Then I should see the map screen
    And I should see the station grid
    And I should see my current position marked
    And I should see the map legend

  Scenario: Switch to help view
    Given I am on any screen
    When I press F4
    Then I should see the help screen
    And I should see command reference
    And I should see keybindings
    And I should see game tips

  Scenario: Switch to chat view
    Given I am on the game screen
    When I press F5
    Then I should see the chat screen
    And I should see multiple channel tabs
    And I should see the online players list
    And I should see the message input field

  Scenario: Return to game view
    Given I am on the inventory screen
    When I press F1
    Then I should see the game screen
    And I should see the terminal log
    And I should see the command input

  Scenario: Rapid view switching
    Given I am on the game screen
    When I press F2, F3, F4, F5, F1 in sequence
    Then each view should load correctly
    And there should be no errors
    And the UI should remain responsive

  Scenario: State preservation across views
    Given I am on the game screen
    And I have typed "some text" in the input
    When I press F2 to go to inventory
    And I press F1 to return to game
    Then the game view should be fresh
    And the input field should be empty
