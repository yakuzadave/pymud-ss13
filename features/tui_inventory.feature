Feature: TUI Inventory Management
  As a player
  I want to manage my inventory through the TUI
  So that I can use, equip, and organize items

  Background:
    Given I am logged into the TUI as "testuser"
    And I am on the inventory screen
    And I have at least one item in my inventory

  Scenario: View item details
    When I click on an item in the carried items list
    Then I should see the item details panel
    And I should see the item name
    And I should see the item description
    And I should see the item type
    And I should see the item weight

  Scenario: Use an item with keyboard shortcut
    Given I have selected an item
    When I press the U key
    Then the item should be used
    And I should see a confirmation message

  Scenario: Equip an item
    Given I have selected an unequipped item
    When I press the E key
    Then the item should move to the equipped list
    And the player stats should update

  Scenario: Unequip an item
    Given I have selected an equipped item
    When I press the E key
    Then the item should move to the carried list
    And the player stats should update

  Scenario: Drop an item
    Given I have selected an item
    When I press the D key
    Then I should see a confirmation prompt
    When I confirm the action
    Then the item should be removed from my inventory
    And the player stats should update

  Scenario: Examine an item
    Given I have selected an item
    When I press the X key
    Then I should see detailed examination text
    And I should see all item properties

  Scenario: Refresh inventory
    When I press the R key
    Then the inventory should refresh from the server
    And I should see any new items
    And I should see updated item states

  Scenario: View player stats
    Then I should see my total weight carried
    And I should see my carrying capacity
    And I should see my item count
    And I should see my credits balance
