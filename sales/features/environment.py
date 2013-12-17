from django.contrib.auth.models import User

from inventory.models import Category, Item, Seller
from sales.models import Tax
from test.bdd.environment import before_all as common_before_all
from test.bdd.environment import *  # Import all common environment functions

def before_all(context):
    common_before_all(context)

    # Create the test user
    user = User(username="test")
    user.set_password("password")
    user.save()

    # Create a category
    category = Category.objects.create(
        user = user,
        name = "Test Category"
    )

    # Create a seller
    seller = Seller.objects.create(
        user = user,
        first_name="Test",
        last_name="User"
    )

    # Create item
    context.item = Item.objects.create(
        user = user,
        number = "1",
        desc = "my desc",
        price = "1.23",
        commission = "10%"
    )
    context.item.categories.add(category)
    context.item.sellers.add(seller)

    # Create a tax rate
    Tax.objects.create(
        county = "Monroe",
        state = "NY",
        sales_tax = 8.0
    )
