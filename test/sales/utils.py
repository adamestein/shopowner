from django.test import TestCase

from sales.utils import calculate_sale_price, round_currency

class UtilsTestCase(TestCase):
    def test_calculate_sale_price(self):
        self.assertEqual(calculate_sale_price(1, 0, 8), 1.08)
        self.assertEqual(calculate_sale_price(5, 20, 4.2), 4.17)
        self.assertEqual(calculate_sale_price(2, 0, 33.75), 2.68)

    def test_round_currency(self):
        self.assertEqual(round_currency(1.08), 1.08)
        self.assertEqual(round_currency(4.168), 4.17)
        self.assertEqual(round_currency(2.675), 2.68)

