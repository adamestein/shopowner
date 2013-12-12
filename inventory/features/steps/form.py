from behave import when, then

@when('I set the {element} to "{value}"')
def impl(context, element, value):
    if element == "description":
        # Easier to read if test says "description" instead of "desc"
        name = "desc"
    else:
        name = element

    context.browser.fill(name, value)

@when('I set the {element} to list item {value}')
def impl(context, element, value):
    context.browser.select(element, value)

@when('I click {button}')
def impl(context, button):
    context.browser.find_by_value(button).first.click()

@then('I see the {what} update page')
def impl(context, what):
    if what == "item":
        text = "The Inventory has been updated."
    else:
        # Unknown update page
        assert False

    assert context.browser.is_text_present(text)

