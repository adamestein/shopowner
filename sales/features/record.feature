Feature: Sales App - Record Sale

    Scenario: Record Sale
        Given the "Record Sale" page
        When I log in
        And I set the item to list item 1
        And I set the date to "1/1/2013"
        And I click Record
        Then I see the record update page
        And the sale has been recorded

