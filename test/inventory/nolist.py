from django.contrib.auth.models import User
from django.test import TestCase

from inventory.models import Item, Seller

class NoList(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("adam", password="password")
        self.client.login(username="adam", password="password")

    def test_item_list(self):
        response = self.client.get("/shopowner/inventory/list/")
        self.assertContains(response, "<p>There are no items to list.</p>", html=True)

        # Create an item so we can test the other edit URL
        Item.objects.create(
            user = self.user,
            number = "1",
            desc = "This is a description",
            price = 123456.78
        )

        response = self.client.get("/shopowner/inventory/list/")
        self.assertNotContains(response, "<p>There are no items to list</p>", html=True)

    def test_seller_list(self):
        response = self.client.get("/shopowner/seller/list/")
        self.assertContains(response, "<p>There are no sellers to list.</p>", html=True)

        Seller.objects.create(
            first_name="Adam",
            last_name="Stein",
            user = self.user
        )

        response = self.client.get("/shopowner/seller/list/")
        self.assertNotContains(response, "<p>There are no sellers to list.</p>", html=True)

