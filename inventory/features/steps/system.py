import decimal

from behave import given, then, when

from inventory.models import Item
from test.utils import almost_equal

@given('the "{page}" page')
def impl(context, page):
    if page == "Add Item":
        context.browser.visit("http://127.0.0.1:8081/shopowner/inventory/add/")
    else:
        # Unknown page
        assert False

@when('I log in')
def impl(context):
    context.browser.fill("username", "test")
    context.browser.fill("password", "password")
    context.browser.find_by_value("login").first.click()

@then('the {object} has been {action}')
def impl(context, object, action):
    if action == "added":
        if object == "item":
            item = Item.objects.get(pk=1)

            assert item.desc == "my desc"
            assert item.categories.get(pk=1).name == "Test Category"
            assert item.sellers.get(pk=1).first_name == "Test" and \
                    item.sellers.get(pk=1).last_name == "User"
            assert almost_equal(item.price, decimal.Decimal(1.23), 0.000001)
            assert item.commission == "10%"
        else:
            # Unknown object
            assert False
    else:
        # Unknown action
        assert False
