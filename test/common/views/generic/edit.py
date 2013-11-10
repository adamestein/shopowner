from django.test import TestCase

from common.views.generic import NavigationCreateView

class EditViewsTestCase(TestCase):
    def test_create_view(self):
        # No navigation view
        view = NavigationCreateView()
        view.object = "blah"
        context = view.get_context_data()

        self.assertEqual("Create", context["action"])
        self.assertEqual(None, context["navigation"])

        # Navigation view = Foo
        view.navigation = "Foo"
        context = view.get_context_data()

        self.assertEqual("Foo", context["navigation"])

