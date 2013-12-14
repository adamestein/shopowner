import decimal

from behave import given, then, when

from inventory.models import Category, Item, Seller
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
    elif page == "Add Seller":
        context.browser.visit(context.config.server_url + "/shopowner/seller/add/")
    elif page == "Edit Seller":
        context.browser.visit(context.config.server_url + "/shopowner/seller/edit/")
    elif page == "List Sellers":
        context.browser.visit(context.config.server_url + "/shopowner/seller/list/")
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
    if object == "category":
        category = Category.objects.get(pk=2)

        if action == "added":
            assert category.name == "my category", "category name = [" + category.name + "]"
            assert category.desc == "my desc", "category description = [" + category.desc + "]"
        elif action == "updated":
            assert category.name == "new name"
            assert category.desc == "new desc"
        else:
            # Unknown action
            assert False
    elif object == "item":
        item = Item.objects.get(pk=1)

        if action == "added":
            assert item.desc == "my desc"
            assert item.categories.get(pk=1).name == "Test Category"
            assert item.sellers.get(pk=1).first_name == "Test" and \
                    item.sellers.get(pk=1).last_name == "User"
            assert almost_equal(item.price, decimal.Decimal(1.23), 0.000001)
            assert item.commission == "10%"
        elif action == "updated":
            assert item.desc == "new description"
            assert item.categories.get(pk=1).name == "Test Category"
            assert item.sellers.get(pk=1).first_name == "Test" and \
                    item.sellers.get(pk=1).last_name == "User"
            assert almost_equal(item.price, decimal.Decimal(5.40), 0.000001)
            assert item.commission == "10%"
        else:
            # Unknown action
            assert False
    elif object == "seller":
        seller = Seller.objects.get(pk=2)

        if action == "added":
            assert seller.first_name == "foo"
            assert seller.last_name == "bar"
        elif action == "updated":
            assert seller.first_name == "Joe"
            assert seller.last_name == "Blow"
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
    elif object == "seller":
        assert context.browser.is_text_present("Sellers (sorted by last name):")
        assert context.browser.is_text_present("Blow, Joe")
        assert context.browser.is_text_present("User, Test")
    else:
        # Unknown object
        assert False

