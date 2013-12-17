from behave import when

@when('I log in')
def login(context):
    context.browser.fill("username", "test")
    context.browser.fill("password", "password")
    context.browser.find_by_value("login").first.click()

