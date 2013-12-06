from django.test import TestCase

from sales.navigation import Navigation

class NavigationTestCase(TestCase):
    def test_no_subject(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["View Sales",          "/shopowner/sales/view/"],
        )

        self.assertEqual(Navigation(""), ans)

    def test_record_sale(self):
        ans = (
            ["Record Sale",         ""],
            ["View Sales",          "/shopowner/sales/view/"],
        )

        self.assertEqual(Navigation("record_sale"), ans)

    def test_view_sales(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["View Sales",          ""],
        )

        self.assertEqual(Navigation("view_sales"), ans)

