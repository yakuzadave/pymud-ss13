Feature: TUI Chat System
  As a player
  I want to communicate with other players through the chat system
  So that I can coordinate and socialize

  Background:
    Given the game server is running
    And the TUI client is launched
    And I am logged into the TUI as "testuser"
    And I am on the game screen

  Scenario: Send a message to global chat
    When I type "say Hello everyone!"
    And I press Enter
    Then I should see "testuser: Hello everyone!" in the chat log
    And other players should receive my message

  Scenario: View chat history
    Given there are 50 messages in chat history
    When I scroll up in the chat panel
    Then I should see older messages
    And the scroll position should be maintained
    When I scroll to the bottom
    Then I should see the most recent messages

  Scenario: Switch to chat view
    When I press F5 to switch to chat view
    Then I should see the chat screen
    And I should see multiple chat channels
    And I should see the message input field
    And I should see the current channel indicator

  Scenario: Switch between chat channels
    Given I am viewing the chat screen
    When I press "1" to switch to global channel
    Then the channel indicator should show "Global"
    And I should see global chat messages
    When I press "2" to switch to local channel
    Then the channel indicator should show "Local"
    And I should see only local chat messages
    When I press "3" to switch to department channel
    Then the channel indicator should show my department name
    And I should see department-specific messages

  Scenario: Send message to specific channel
    Given I am viewing the chat screen
    And I am on the department channel
    When I type "Meeting in 5 minutes"
    And I press Enter
    Then the message should appear in department channel
    And only department members should see the message

  Scenario: Private message to another player
    When I type "pm engineer Hey, need help with power"
    And I press Enter
    Then I should see "PM to engineer: Hey, need help with power"
    And the engineer should receive a private message notification

  Scenario: Receive private message
    When another player sends me a private message
    Then I should see a notification indicator
    And the message should appear in my PM tab
    And I should hear a notification sound

  Scenario: Filter chat by message type
    Given I am viewing the chat screen
    When I press "F" to open filter menu
    And I select "System messages only"
    Then I should only see system messages
    When I select "Show all messages"
    Then I should see all message types again

  Scenario: Mute a player
    Given I am viewing the chat screen
    When I right-click on "spammer123" in the player list
    And I select "Mute player"
    Then messages from "spammer123" should be hidden
    And I should see "Player muted: spammer123" confirmation

  Scenario: View online players in chat
    Given I am viewing the chat screen
    When I look at the player list sidebar
    Then I should see all online players
    And I should see their current status
    And I should see their job roles

  Scenario: Chat notifications while in other views
    Given I am on the game screen
    When I receive a new chat message
    Then I should see a chat notification badge
    And the notification count should increase
    When I switch to chat view
    Then the notification badge should clear

  Scenario: Use emotes in chat
    When I type "emote waves"
    And I press Enter
    Then I should see "testuser waves" in the chat
    And it should be styled differently from regular messages

  Scenario: Command autocomplete in chat
    Given I am in the chat input field
    When I type "/help"
    Then I should see autocomplete suggestions
    And I should see available chat commands listed
    When I press Tab
    Then the command should autocomplete

  Scenario: Chat message timestamp display
    Given I am viewing the chat screen
    When I look at the chat messages
    Then each message should have a timestamp
    And timestamps should be in "HH:MM" format
    And recent messages should show relative time

  Scenario: Return to game from chat
    Given I am viewing the chat screen
    When I press F1 to switch to game view
    Then I should return to the game screen
    And unread messages should still show in notification badge
