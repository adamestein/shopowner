import datetime
import decimal

from behave import given, then
from django.contrib.auth.models import User

from sales.models import Sale, Tax
from test.utils import almost_equal

@given('the "{page}" page')
def impl(context, page):
    if page == "Record Sale":
        context.browser.visit(context.config.server_url + "/shopowner/sales/record/")
    elif page == "View Sales":
        context.browser.visit(context.config.server_url + "/shopowner/sales/view/")
    else:
        # Unknown page
        assert False

@then('the {thing} has been {action}')
def impl(context, thing, action):
    if thing == "sale":
        sale = Sale.objects.get(pk=1)

        assert sale.item == context.item1
        assert sale.tax_rate == 8.0
        assert sale.discount == 0.0
        assert almost_equal(sale.price, decimal.Decimal(1.33), 0.000001)
        assert almost_equal(sale.commission, decimal.Decimal(0.06), 0.000001)
        assert str(sale.date) == "2013-01-01"
    else:
        # Unknown thing
        assert False

@then('I see the {what} update page')
def impl(context, what):
    if what == "record":
        text = "The sale has been recorded."
    else:
        # Unknown update page
        assert False

    assert context.browser.is_text_present(text)

@then('I see the "{what}" warning popup')
def impl(context, what):
    if what == "tax rate":
        assert context.browser.is_text_present("Can't automatically calculate price or commission without the tax rate.") 
    else:
        # Unknown what
        assert False

@given('the default tax rate')
def impl(context):
    Tax.objects.create(
        county = "Monroe",
        state = "NY",
        sales_tax = 8.0
    )

@given('no tax rate')
def impl(context):
    Tax.objects.get(pk=1).delete()

@given('some sales')
def impl(context):
    # Delete any existing sales records (start fresh)
    Sale.objects.all().delete()

    # Create some sales so we can view them
    Sale.objects.create(
        user = User.objects.get(username="test"),
        item = context.item1,
        tax_rate = 8,
        discount = 0,
        price = 6.67,
        commission = 0.25,
        date = datetime.datetime(2013, 11, 15)
    )

    Sale.objects.create(
        user = User.objects.get(username="test"),
        item = context.item2,
        tax_rate = 4,
        discount = 5,
        price = 1.23,
        commission = 0.75,
        date = datetime.datetime(2013, 11, 15)
    )

    Sale.objects.create(
        user = User.objects.get(username="test"),
        item = context.item4,
        tax_rate = 4,
        discount = 5,
        price = 1.23,
        date = datetime.datetime(2013, 11, 15)
    )

    Sale.objects.create(
        user = User.objects.get(username="test"),
        item = context.item5,
        tax_rate = 4,
        discount = 5,
        price = 1.23,
        commission=0,
        date = datetime.datetime(2013, 11, 15)
    )

@then('I see the table view')
def impl(context):
    present = context.browser.is_text_present
    not_present = context.browser.is_text_not_present

    assert present("my desc 1")
    assert present("6.67")
    assert present("0.25")
    assert present("8.0%")

    assert present("my desc 2")
    assert present("1.23")
    assert present("0.75")
    assert present("4.0%")

    assert present("my desc 4")
    assert not_present("None")

    assert present("my desc 5")
    assert present("N/A")


