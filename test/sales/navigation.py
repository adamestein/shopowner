from django.test import TestCase

from sales.navigation import Navigation

class NavigationTestCase(TestCase):
    def test_no_subject(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["View Sales",          "/shopowner/sales/view/"],
            ["",                    ""],
            ["Update Sales Tax",    "/shopowner/sales/update/tax/"],
        )

        self.assertEqual(Navigation(""), ans)

    def test_record_sale(self):
        ans = (
            ["Record Sale",         ""],
            ["View Sales",          "/shopowner/sales/view/"],
            ["",                    ""],
            ["Update Sales Tax",    "/shopowner/sales/update/tax/"],
        )

        self.assertEqual(Navigation("record_sale"), ans)

    def test_view_sales(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["View Sales",          ""],
            ["",                    ""],
            ["Update Sales Tax",    "/shopowner/sales/update/tax/"],
        )

        self.assertEqual(Navigation("view_sales"), ans)

    def test_update_sales_tax(self):
        ans = (
            ["Record Sale",         "/shopowner/sales/record/"],
            ["View Sales",          "/shopowner/sales/view/"],
            ["",                    ""],
            ["Update Sales Tax",    ""],
        )

        self.assertEqual(Navigation("update_sales_tax"), ans)

    def footest_add_seller(self):
        ans = (
            ["Add Item",        "/shopowner/inventory/add/"],
            ["Edit Item",       "/shopowner/inventory/edit/"],
            ["List Items",      "/shopowner/inventory/list/"],
            ["",                ""],
            ["Add Seller",      ""],
            ["Edit Seller",     "/shopowner/seller/edit/"],
            ["List Sellers",    "/shopowner/seller/list/"],
        )

        self.assertEqual(Navigation("add_seller"), ans)

    def footest_edit_seller(self):
        ans = (
            ["Add Item",        "/shopowner/inventory/add/"],
            ["Edit Item",       "/shopowner/inventory/edit/"],
            ["List Items",      "/shopowner/inventory/list/"],
            ["",                ""],
            ["Add Seller",      "/shopowner/seller/add/"],
            ["Edit Seller",     ""],
            ["List Sellers",    "/shopowner/seller/list/"],
        )

        self.assertEqual(Navigation("edit_seller"), ans)

    def footest_list_sellers(self):
        ans = (
            ["Add Item",        "/shopowner/inventory/add/"],
            ["Edit Item",       "/shopowner/inventory/edit/"],
            ["List Items",      "/shopowner/inventory/list/"],
            ["",                ""],
            ["Add Seller",      "/shopowner/seller/add/"],
            ["Edit Seller",     "/shopowner/seller/edit/"],
            ["List Sellers",    ""],
        )

        self.assertEqual(Navigation("list_sellers"), ans)

