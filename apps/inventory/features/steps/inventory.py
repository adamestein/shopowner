import decimal

# noinspection PyUnresolvedReferences
from behave import given, then

from inventory.models import Category, Item, Seller
from test.utils import almost_equal


@given('the {page} page')
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

@then('the {thing} has been {action}')
def impl(context, thing, action):
    if thing == "category":
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
    elif thing == "item":
        item = Item.objects.get(pk=1)

        if action == "added":
            assert item.desc == "my desc"
            assert item.category.name == "Test Category"
            assert item.sellers.get(pk=1).first_name == "Test" and \
                item.sellers.get(pk=1).last_name == "User"
            assert almost_equal(item.price, decimal.Decimal(1.23), 0.000001)
            assert item.commission == "10%"
        elif action == "updated":
            assert item.desc == "new description"
            assert item.category.name == "Test Category"
            assert item.sellers.get(pk=1).first_name == "Test" and \
                item.sellers.get(pk=1).last_name == "User"
            assert almost_equal(item.price, decimal.Decimal(5.40), 0.000001)
            assert item.commission == "10%"
        else:
            # Unknown action
            assert False
    elif thing == "seller":
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

@then('I see the {thing} list')
def impl(context, thing):
    find_text = context.browser.is_text_present

    if thing == "category":
        assert find_text("Categories (sorted by name):")
        assert find_text("Test Category")
        assert find_text("new name (new desc)")
    elif thing == "item":
        assert find_text("new description")
        assert find_text("$5.40")
        assert find_text("Unsold")
    elif thing == "seller":
        assert find_text("Sellers (sorted by last name):")
        assert find_text("Blow, Joe")
        assert find_text("User, Test")
    else:
        # Unknown thing
        assert False

@then('I see the {what} update page')
def impl(context, what):
    if what == "category":
        text = "The Category List has been updated."
    elif what == "item":
        text = "The Inventory has been updated."
    elif what == "seller":
        text = "The Sellers List has been updated."
    else:
        # Unknown update page
        assert False

    assert context.browser.is_text_present(text)

@then('I see the {what} form again')
def impl(context, what):
    if what == "category":
        text = "Category List has been updated"
    elif what == "item":
        text = "Inventory has been updated"
    elif what == "seller":
        text = "Sellers List has been updated"
    else:
        # Unknown update page
        assert False

    assert context.browser.is_text_present(text)
