Feature: Inventory App - Items

    Scenario: Add Item
        Given the Add Item page
        When I log in
        And I set the description to my desc
        And I set the category to list item 1
        And I set the sellers to list item 1
        And I set the price to 1.23
        And I set the commission to 10%
        And I click Add
        Then I see the item form again
        And the item has been added

    Scenario: Edit Item
        Given the Edit Item page
        When I set the item to list item 1
        And I set the description to new description
        And I set the price to 5.40
        And I click Update
        Then I see the item update page
        And the item has been updated

    Scenario: List Items
        Given the List Items page
        Then I see the item list

