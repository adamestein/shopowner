import logging

from splinter.browser import Browser
from django.contrib.auth.models import User

from inventory.models import Category, Seller

def before_all(context):
    # In case logging is not captured
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

    # Default to firefox if not set
    browser = "firefox" if not context.config.browser else context.config.browser

    context.browser = Browser(browser)

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

def after_all(context):
    context.browser.quit()
    context.browser = None

