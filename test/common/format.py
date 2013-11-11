from django.test import TestCase

from common.format import currency, with_commas

class FormatTestCase(TestCase):
    def test_currency(self):
        self.assertEqual(currency(1.23), "$1.23")
        self.assertEqual(currency(12345), "$12,345.00")
        self.assertEqual(currency(12345.6789), "$12,345.68")

    def test_with_commas(self):
        # Default precision
        self.assertEqual(with_commas(1.23), "1.230000")
        self.assertEqual(with_commas(12345), "12,345.000000")
        self.assertEqual(with_commas(12345.6789), "12,345.678900")

        # Precision = 2
        self.assertEqual(with_commas(1.23, 2), "1.23")
        self.assertEqual(with_commas(12345, 2), "12,345.00")
        self.assertEqual(with_commas(12345.6789, 2), "12,345.68")

