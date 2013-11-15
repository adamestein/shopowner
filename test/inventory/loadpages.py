import inspect

from django.contrib.auth.models import User
from django.test import TestCase

from inventory.models import Item, Seller

class LoadPages(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("adam", password="password")
        self.client.logout()

    def test_home_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/inventory/")
        
        # Make sure page used the correct template
        self._template_test("/shopowner/inventory/", "inventory_home.html")

    def test_add_item_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/inventory/add/")

        # Make sure page used the correct template
        self._template_test("/shopowner/inventory/add/", "item_form.html")

    def test_edit_item_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/inventory/edit/")

        # Make sure page used the correct template
        self._template_test("/shopowner/inventory/edit/", "item_edit_list.html")

        # Logout to force the other edit URL to need to log in
        self.client.logout()

        # Create an item so we can test the other edit URL
        Item.objects.create(
            user = self.user,
            number = "1",
            desc = "This is a description",
            price = 123456.78
        )

        # Test that you need to login to see this page
        self._login_test("/shopowner/inventory/edit/1")

        # Make sure page used the correct template
        self._template_test("/shopowner/inventory/edit/1", "item_form.html")

    def test_list_item_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/inventory/list/")
        
        # Make sure page used the correct template
        self._template_test("/shopowner/inventory/list/", "item_list.html")

    def test_add_seller_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/seller/add/")
        
        # Make sure page used the correct template
        self._template_test("/shopowner/seller/add/", "seller_form.html")

    def test_edit_seller_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/seller/edit/")

        # Make sure page used the correct template
        self._template_test("/shopowner/seller/edit/", "seller_edit_list.html")

        # Logout to force the other edit URL to need to log in
        self.client.logout()

        # Create an item so we can test the other edit URL
        Seller.objects.create(
            first_name="Adam",
            last_name="Stein",
            user = self.user
        )

        # Test that you need to login to see this page
        self._login_test("/shopowner/seller/edit/1")

        # Make sure page used the correct template
        self._template_test("/shopowner/seller/edit/1", "seller_form.html")

    def test_list_seller_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/seller/list/")
        
        # Make sure page used the correct template
        self._template_test("/shopowner/seller/list/", "seller_list.html")

    def _login_test(self, url):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        prefix = calframe[1][3]

        response = self.client.get(url)
        self.assertRedirects(
            response,
            "/shopowner/accounts/login/?next=" + url,
            msg_prefix=prefix
        )

        self.client.login(username="adam", password="password")

    def _template_test(self, url, template):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        prefix = calframe[1][3]

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, msg=prefix)
        self.assertTemplateUsed(response, template, msg_prefix=prefix)

