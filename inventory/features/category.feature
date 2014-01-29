Feature: Inventory App - Categories

    Scenario: Add Category
        Given the Add Category page
        When I log in
        And I set the name to my category
        And I set the description to my desc
        And I click Add
        Then I see the category form again
        And the category has been added

    Scenario: Edit Category
        Given the Edit Category page
        When I set the categories to list item 2
        And I set the name to new name
        And I set the desc to new desc
        And I click Update
        Then I see the category update page
        And the category has been updated

    Scenario: List Categories
        Given the List Categories page
        Then I see the category list

