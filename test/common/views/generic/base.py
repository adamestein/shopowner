from django.test import TestCase

from common.views.generic import NavigationTemplateView

class BaseViewsTestCase(TestCase):
    def test_template_view(self):
        # No navigation view
        view = NavigationTemplateView()
        context = view.get_context_data()

        self.assertEqual(None, context["navigation"])

        # Navigation view = Foo
        view.navigation = "Foo"
        context = view.get_context_data()

        self.assertEqual("Foo", context["navigation"])

