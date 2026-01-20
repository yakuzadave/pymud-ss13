Feature: TUI Help System
  As a player
  I want to access game help and documentation in the TUI
  So that I can learn how to play effectively

  Background:
    Given the game server is running
    And the TUI client is launched
    And I am logged into the TUI as "testuser"
    And I am on the game screen

  Scenario: Open help screen
    When I press F4 to switch to help view
    Then I should see the help screen
    And I should see the help categories menu
    And I should see a search box
    And I should see quick reference shortcuts

  Scenario: Browse help categories
    Given I am viewing the help screen
    When I click on "Basic Commands" category
    Then I should see a list of basic commands
    And each command should have a description
    And each command should have usage examples

  Scenario: View command details
    Given I am viewing the help screen
    And I am in the "Basic Commands" category
    When I click on the "look" command
    Then I should see detailed command information
    And I should see command syntax
    And I should see command parameters
    And I should see usage examples
    And I should see related commands

  Scenario: Search for help topics
    Given I am viewing the help screen
    When I type "inventory" in the search box
    Then I should see search results for "inventory"
    And results should be ranked by relevance
    And I should see matching commands and articles
    When I click on a search result
    Then I should navigate to that help topic

  Scenario: View keyboard shortcuts reference
    Given I am viewing the help screen
    When I click on "Keyboard Shortcuts" category
    Then I should see a list of all keyboard shortcuts
    And shortcuts should be grouped by function
    And I should see F1-F5 view switching shortcuts
    And I should see movement and action shortcuts

  Scenario: View job-specific help
    Given I am viewing the help screen
    And my job is "Engineer"
    When I click on "Job Guides" category
    Then I should see my job highlighted
    When I click on "Engineer" guide
    Then I should see engineer-specific instructions
    And I should see engineer equipment list
    And I should see engineer responsibilities

  Scenario: View game mechanics explanation
    Given I am viewing the help screen
    When I click on "Game Mechanics" category
    Then I should see topics like "Atmosphere", "Power", "Combat"
    When I click on "Atmosphere" topic
    Then I should see detailed atmosphere mechanics explanation
    And I should see related systems documentation

  Scenario: Copy command examples
    Given I am viewing the help screen
    And I am viewing a command with examples
    When I click "Copy" next to an example
    Then the example should be copied to clipboard
    And I should see "Copied to clipboard" confirmation

  Scenario: Navigate help history
    Given I am viewing the help screen
    And I have viewed multiple help pages
    When I press the back button
    Then I should return to the previous help page
    When I press the forward button
    Then I should go forward in help history

  Scenario: View getting started tutorial
    Given I am viewing the help screen
    And I am a new player
    When I click on "Getting Started" tutorial
    Then I should see step-by-step instructions
    And I should see tutorial progress indicator
    And I should be able to navigate between tutorial steps

  Scenario: Access context-sensitive help
    Given I am on the game screen
    And I have selected an item in my inventory
    When I press F4 to open help
    Then the help should open to item usage information
    And I should see how to use the selected item

  Scenario: View recent updates and patch notes
    Given I am viewing the help screen
    When I click on "What's New" category
    Then I should see recent game updates
    And I should see patch notes
    And updates should be sorted by date

  Scenario: Export help content
    Given I am viewing the help screen
    When I click "Export to File"
    Then I should see export options
    And I should be able to save help as text file
    And the file should contain all help content

  Scenario: Help screen quick navigation
    Given I am viewing the help screen
    When I press a letter key
    Then the help should jump to topics starting with that letter
    When I press "/" to search
    Then the search box should be focused

  Scenario: View command aliases
    Given I am viewing the help screen
    When I view the "look" command details
    Then I should see command aliases listed
    And I should see "l" as an alias for "look"
    And aliases should be clickable to view details

  Scenario: Return to game from help
    Given I am viewing the help screen
    When I press F1 to switch to game view
    Then I should return to the game screen
    And my help browsing position should be saved
    When I press F4 again
    Then I should return to the same help page
