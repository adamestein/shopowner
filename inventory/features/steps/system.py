import decimal

from behave import given, then, when

from inventory.models import Category, Item
from test.utils import almost_equal

@given('the "{page}" page')
def impl(context, page):
    if page == "Add Item":
        context.browser.visit(context.config.server_url + "/shopowner/inventory/add/")
    elif page == "Edit Item":
        context.browser.visit(context.config.server_url + "/shopowner/inventory/edit/")
    elif page == "List Items":
        context.browser.visit(context.config.server_url + "/shopowner/inventory/list/")
    elif page == "Add Category":
        context.browser.visit(context.config.server_url + "/shopowner/category/add/")
    elif page == "Edit Category":
        context.browser.visit(context.config.server_url + "/shopowner/category/edit/")
    elif page == "List Categories":
        context.browser.visit(context.config.server_url + "/shopowner/category/list/")
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
        if object == "category":
            category = Category.objects.get(pk=2)

            assert category.name == "my category", "category name = [" + category.name + "]"
            assert category.desc == "my desc", "category description = [" + category.desc + "]"
        elif object == "item":
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
    elif action == "updated":
        if object == "item":
            item = Item.objects.get(pk=1)

            assert item.desc == "new description"
            assert item.categories.get(pk=1).name == "Test Category"
            assert item.sellers.get(pk=1).first_name == "Test" and \
                    item.sellers.get(pk=1).last_name == "User"
            assert almost_equal(item.price, decimal.Decimal(5.40), 0.000001)
            assert item.commission == "10%"
    else:
        # Unknown action
        assert False

@then('I see the {object} list')
def impl(context, object):
    if object == "category":
        assert context.browser.is_text_present("Categories (sorted by name):")
        assert context.browser.is_text_present("Test Category")
        assert context.browser.is_text_present("new name (new desc)")
    elif object == "item":
        assert context.browser.is_text_present("new description")
        assert context.browser.is_text_present("$5.40")
        assert context.browser.is_text_present("Unsold")
    else:
        # Unknown object
        assert False

