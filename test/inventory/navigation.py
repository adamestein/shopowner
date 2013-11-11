from django.test import TestCase

from inventory.navigation import Navigation

class NavigationTestCase(TestCase):
    def test_no_subject(self):
        ans = (
            ["Add Item",        "/shopowner/inventory/add/"],
            ["Edit Item",       "/shopowner/inventory/edit/"],
            ["List Items",      "/shopowner/inventory/list/"],
            ["",                ""],
            ["Add Seller",      "/shopowner/seller/add/"],
            ["Edit Seller",     "/shopowner/seller/edit/"],
            ["List Sellers",    "/shopowner/seller/list/"],
        )

        self.assertEqual(Navigation(""), ans)

    def test_add_item(self):
        ans = (
            ["Add Item",        ""],
            ["Edit Item",       "/shopowner/inventory/edit/"],
            ["List Items",      "/shopowner/inventory/list/"],
            ["",                ""],
            ["Add Seller",      "/shopowner/seller/add/"],
            ["Edit Seller",     "/shopowner/seller/edit/"],
            ["List Sellers",    "/shopowner/seller/list/"],
        )

        self.assertEqual(Navigation("add_item"), ans)

    def test_edit_item(self):
        ans = (
            ["Add Item",        "/shopowner/inventory/add/"],
            ["Edit Item",       ""],
            ["List Items",      "/shopowner/inventory/list/"],
            ["",                ""],
            ["Add Seller",      "/shopowner/seller/add/"],
            ["Edit Seller",     "/shopowner/seller/edit/"],
            ["List Sellers",    "/shopowner/seller/list/"],
        )

        self.assertEqual(Navigation("edit_item"), ans)

    def test_list_items(self):
        ans = (
            ["Add Item",        "/shopowner/inventory/add/"],
            ["Edit Item",       "/shopowner/inventory/edit/"],
            ["List Items",      ""],
            ["",                ""],
            ["Add Seller",      "/shopowner/seller/add/"],
            ["Edit Seller",     "/shopowner/seller/edit/"],
            ["List Sellers",    "/shopowner/seller/list/"],
        )

        self.assertEqual(Navigation("list_items"), ans)

    def test_add_seller(self):
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

    def test_edit_seller(self):
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

    def test_list_sellers(self):
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

