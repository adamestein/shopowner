import time

from behave import when

@when('I set the {element} to "{value}"')
def set_element(context, element, value):
    if element == "description":
        # Easier to read if test says "description" instead of "desc"
        name = "desc"
    else:
        name = element

    context.browser.fill(name, value)

    if name == "date":
        # Click somewhere else to remove the calendar popup
        context.browser.find_by_tag("h1").click()
        time.sleep(2)   # Time for popup to disappear

@when('I set the {element} to list item {value}')
def set_list_element(context, element, value):
    context.browser.select(element, value)

@when('I click {button}')
def click_button(context, button):
    context.browser.find_by_value(button).first.click()

