from django.contrib.auth.models import User

from inventory.models import Category, Seller
from test.bdd.environment import before_all as common_before_all
from test.bdd.environment import *  # Import all common environment functions

def before_all(context):
    common_before_all(context)

    # Create the test user
    user = User(username="test")
    user.set_password("password")
    user.save()

    # Create a category
    Category.objects.create(
        user = user,
        name = "Test Category"
    )

    # Create a seller
    Seller.objects.create(
        user = user,
        first_name="Test",
        last_name="User"
    )

