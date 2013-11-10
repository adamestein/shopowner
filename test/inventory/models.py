from django.contrib.auth.models import User
from django.test import TestCase

from inventory.models import Item, Seller

class HumanReadableModelTestCase(TestCase):
    def test_Item(self):
        item = Item.objects.create(
            user = User.objects.create_user("adam"),
            number = "101a",
            desc = "This is a description",
            price = 123456.78
        )
        self.assertEqual("101a: This is a description ($123,456.78)", str(item))

    def test_Seller(self):
        seller = Seller.objects.create(first_name="Adam", last_name="Stein")
        self.assertEqual("Stein, Adam", str(seller))
