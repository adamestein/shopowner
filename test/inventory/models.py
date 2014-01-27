from django.contrib.auth.models import User
from django.test import TestCase

from inventory.models import Item, Seller


class HumanReadableModelTestCase(TestCase):
    def setUp(self):
        super(HumanReadableModelTestCase, self).setUp()

        self.user = User.objects.create_user("adam")

    def test_Item(self):
        item = Item.objects.create(
            user=self.user,
            number=101,
            desc="This is a description",
            price=123456.78
        )
        self.assertEqual("101: This is a description ($123,456.78)", str(item))

    def test_Seller(self):
        seller = Seller.objects.create(
            first_name="Adam",
            last_name="Stein",
            user=self.user
        )
        self.assertEqual("Stein, Adam", str(seller))
