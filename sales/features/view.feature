Feature: Sales App - View Sales

    Scenario: View sales in table form
        Given some sales
        And the "View Sales" page
        When I log in
        Then I see the table view

