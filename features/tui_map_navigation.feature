Feature: TUI Map Navigation
  As a player
  I want to navigate and interact with the station map in the TUI
  So that I can visualize my location and surroundings

  Background:
    Given the game server is running
    And the TUI client is launched
    And I am logged into the TUI as "testuser"
    And I am on the game screen

  Scenario: View the station map
    When I press F3 to switch to map view
    Then I should see the map screen
    And I should see the station grid layout
    And I should see my player position marked on the map
    And I should see room labels

  Scenario: Navigate map with arrow keys
    Given I am viewing the map screen
    When I press the right arrow key
    Then the map viewport should scroll right
    When I press the down arrow key
    Then the map viewport should scroll down
    When I press the left arrow key
    Then the map viewport should scroll left
    When I press the up arrow key
    Then the map viewport should scroll up

  Scenario: View room details on map
    Given I am viewing the map screen
    When I click on a room tile
    Then I should see room details in the sidebar
    And I should see the room name
    And I should see room occupants list
    And I should see room exit directions

  Scenario: Toggle map overlays
    Given I am viewing the map screen
    When I press "D" to toggle door overlay
    Then I should see door lock indicators on the map
    When I press "A" to toggle atmosphere overlay
    Then I should see atmosphere status indicators
    When I press "P" to toggle power overlay
    Then I should see power status indicators

  Scenario: Zoom map in and out
    Given I am viewing the map screen
    When I press "+" to zoom in
    Then the map tiles should appear larger
    And I should see fewer rooms on screen
    When I press "-" to zoom out
    Then the map tiles should appear smaller
    And I should see more rooms on screen

  Scenario: Center map on player
    Given I am viewing the map screen
    And I have scrolled away from my position
    When I press "C" to center on player
    Then the map should scroll to show my player position
    And my player marker should be centered on screen

  Scenario: Show minimap indicator
    Given I am on the game screen
    When I look at the corner of the screen
    Then I should see a minimap indicator
    And the minimap should show nearby rooms
    And my current position should be highlighted

  Scenario: Map updates in real-time
    Given I am viewing the map screen
    When another player moves to a new room
    Then I should see their marker update on the map
    When a door lock status changes
    Then the door indicator should update immediately

  Scenario: Return to game from map
    Given I am viewing the map screen
    When I press F1 to switch to game view
    Then I should return to the game screen
    And the map state should be preserved for next view
