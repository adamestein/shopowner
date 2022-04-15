from django.contrib.auth.models import User

from inventory.models import Category, Item, Seller
from test.bdd.environment import before_all as common_before_all
# noinspection PyUnresolvedReferences
from test.bdd.environment import *  # Import all common environment functions


def before_all(context):
    common_before_all(context)

    # Create the test user
    user = User(username="test")
    user.set_password("password")
    user.save()

    # Create a category
    category = Category.objects.create(
        user=user,
        name="Test Category"
    )

    # Create a seller
    seller = Seller.objects.create(
        user=user,
        first_name="Test",
        last_name="User"
    )

    context.item1 = Item.objects.create(
        user=user,
        number="1",
        desc="my desc 1",
        price="1.23",
        category=category,
        commission="5%"
    )
    context.item1.sellers.add(seller)

    context.item2 = Item.objects.create(
        user=user,
        number="2",
        desc="my desc 2",
        price="1.23",
        category=category,
        commission="10%"
    )
    context.item2.sellers.add(seller)

    context.item3 = Item.objects.create(
        user=user,
        number="3",
        desc="my desc 3",
        price="1.23",
        category=category,
        commission="0"
    )
    context.item3.sellers.add(seller)

    context.item4 = Item.objects.create(
        user=user,
        number="4",
        desc="my desc 4",
        price="1.23",
        category=category
    )
    context.item4.sellers.add(seller)

    context.item5 = Item.objects.create(
        user=user,
        number="5",
        desc="my desc 5",
        price="1.23",
        category=category
    )
    context.item5.sellers.add(seller)