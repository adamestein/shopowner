from django.test import TestCase

from sales.utils import calculate_sale_price

class UtilsTestCase(TestCase):
    def test_calculate_sale_price(self):
        self.assertEqual(calculate_sale_price(1, 0, 8), 1.08)
        self.assertEqual(calculate_sale_price(5, 20, 4.2), 4.17)
        self.assertEqual(calculate_sale_price(2, 0, 33.75), 2.68)

