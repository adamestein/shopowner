from django.contrib.auth.models import User
from django.test import TestCase

from common.views.generic import NavigationListView

class ListViewsTestCase(TestCase):
    def test_list_view(self):
        # No navigation view
        view = NavigationListView()
        context = view.get_context_data(object_list=User)

        self.assertEqual(None, context["navigation"])

        # Navigation view = Foo
        view.navigation = "Foo"
        context = view.get_context_data(object_list=User)

        self.assertEqual("Foo", context["navigation"])

