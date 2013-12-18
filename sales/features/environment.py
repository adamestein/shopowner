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

    # Create item for scenario 1
    context.item1 = Item.objects.create(
        user = user,
        number = "1",
        desc = "my desc",
        price = "1.23",
        commission = "10%"
    )
    context.item1.categories.add(category)
    context.item1.sellers.add(seller)

    # Create item for scenario 2
    context.item2 = Item.objects.create(
        user = user,
        number = "2",
        desc = "my desc",
        price = "1.23",
        commission = "10%"
    )
    context.item2.categories.add(category)
    context.item2.sellers.add(seller)

