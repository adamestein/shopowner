Feature: Inventory App

    Scenario: Add Item
        Given the "Add Item" page
        When I log in
        And I set the description to "my desc"
        And I set the categories to list item 1
        And I set the sellers to list item 1
        And I set the price to "1.23"
        And I set the commission to "10%"
        And I click Add
        Then I see the item update page
        And the item has been added

