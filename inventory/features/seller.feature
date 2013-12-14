Feature: Inventory App - Sellers

    Scenario: Add Seller
        Given the "Add Seller" page
        When I log in
        And I set the first_name to "foo"
        And I set the last_name to "bar"
        And I click Add
        Then I see the seller update page
        And the seller has been added

    Scenario: Edit Seller
        Given the "Edit Seller" page
        When I set the sellers to list item 2
        And I set the first_name to "Joe"
        And I set the last_name to "Blow"
        And I click Update
        Then I see the seller update page
        And the seller has been updated

    Scenario: List Sellers
        Given the "List Sellers" page
        Then I see the seller list

