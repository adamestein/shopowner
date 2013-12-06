import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from inventory.models import Item
from sales.models import Sale, Tax

class HumanReadableModelTestCase(TestCase):
    def setUp(self):
        super(HumanReadableModelTestCase, self).setUp()

        self.user = User.objects.create_user("adam")

    def test_Tax(self):
        tax = Tax.objects.create(
            county = "Monroe",
            state = "NY",
            sales_tax = 8
        )
        self.assertEqual("NY, Monroe County = 8.00%", str(tax))

    def test_Sale(self):
        item = Item.objects.create(
            user = self.user,
            number = "1",
            desc = "Description",
            price = 1.23,
            commission = "0"
        )

        sale = Sale.objects.create(
            user = self.user,
            item = item,
            tax_rate = 8,
            discount = 0,
            price = 1.23,
            commission = "0",
            date = datetime.datetime(2013, 11, 15)
        )
        self.assertEqual("'Description' sold for $1.23 on 11/15/2013", str(sale))

