from django.test import TestCase

from sales.navigation import navigation

class NavigationTestCase(TestCase):
    def test_no_subject(self):
        ans = (
            ["Record Sale", "/shopowner/sales/record/"],
            ["Edit Sale", "/shopowner/sales/edit/"],
            ["", ""],
            ["View Sales", "/shopowner/sales/view/"],
        )

        self.assertEqual(navigation(""), ans)

    def test_record_sale(self):
        ans = (
            ["Record Sale",         ""],
            ["Edit Sale", "/shopowner/sales/edit/"],
            ["", ""],
            ["View Sales",          "/shopowner/sales/view/"],
        )

        self.assertEqual(navigation("record_sale"), ans)

    def test_edit_sale(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["Edit Sale", ""],
            ["", ""],
            ["View Sales",          "/shopowner/sales/view/"],
        )

        self.assertEqual(navigation("edit_sale"), ans)

    def test_view_sales(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["Edit Sale", "/shopowner/sales/edit/"],
            ["", ""],
            ["View Sales",          ""],
        )

        self.assertEqual(navigation("view_sales"), ans)

