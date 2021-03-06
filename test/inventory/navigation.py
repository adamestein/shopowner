from django.test import TestCase

from inventory.navigation import navigation


class NavigationTestCase(TestCase):
    def test_no_subject(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation(""), ans)

    def test_add_item(self):
        ans = (
            ["Add Item", ""],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("add_item"), ans)

    def test_edit_item(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", ""],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("edit_item"), ans)

    def test_list_items(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", ""],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("list_items"), ans)

    def test_add_category(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", ""],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("add_category"), ans)

    def test_edit_category(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", ""],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("edit_category"), ans)

    def test_list_categories(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", ""],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("list_categories"), ans)

    def test_add_seller(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", ""],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("add_seller"), ans)

    def test_edit_seller(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", ""],
            ["List Sellers", "/shopowner/seller/list/"],
        )

        self.assertEqual(navigation("edit_seller"), ans)

    def test_list_sellers(self):
        ans = (
            ["Add Item", "/shopowner/inventory/add/"],
            ["Edit Item", "/shopowner/inventory/edit/"],
            ["List Items", "/shopowner/inventory/list/"],
            ["", ""],
            ["Add Category", "/shopowner/category/add/"],
            ["Edit Category", "/shopowner/category/edit/"],
            ["List Categories", "/shopowner/category/list/"],
            ["", ""],
            ["Add Seller", "/shopowner/seller/add/"],
            ["Edit Seller", "/shopowner/seller/edit/"],
            ["List Sellers", ""],
        )

        self.assertEqual(navigation("list_sellers"), ans)

