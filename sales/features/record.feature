Feature: Sales App - Record Sale

    Scenario: Record Sale
        Given the "Record Sale" page
        And the default tax rate
        When I log in
        And I set the item to list item 1
        And I set the date to "1/1/2013"
        And I click Record
        Then I see the record form again
        And the sale has been recorded

    Scenario: Record Sale with no date
        Given the "Record Sale" page
        When I set the item to list item 2
        And I click Record
        Then I see the record form again
        And the sale has been recorded

    Scenario: No commission set
        Given the "Record Sale" page
        When I set the item to list item 4
        And I see the commission set to N/A
        And I set the date to "1/1/2013"
        And I click Record
        Then I see the record form again
        And the sale has been recorded

    Scenario: No tax rate
        Given no tax rate
        And the "Record Sale" page
        When I set the item to list item 3
        Then I see the "tax rate" warning popup