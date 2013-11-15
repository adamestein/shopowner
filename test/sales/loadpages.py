import inspect

from django.contrib.auth.models import User
from django.test import TestCase

class LoadPages(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("adam", password="password")
        self.client.logout()

    def test_home_page(self):
        # Test that you need to login to see this page
        self._login_test("/shopowner/sales/")
        
        # Make sure page used the correct template
        self._template_test("/shopowner/sales/", "sales_home.html")

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

