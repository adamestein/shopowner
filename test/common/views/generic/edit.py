import os

from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase

from common.views.generic import NavigationCreateView, NavigationFormView, NavigationUpdateView

class EditViewsTestCase(TestCase):
    def test_create_view(self):
        # No navigation view
        view = NavigationCreateView()
        view.object = "blah"
        environ = os.environ
        environ.update({
            "REQUEST_METHOD": "get",
            "wsgi.input": "input"
        })
        view.request = WSGIRequest(environ)
        context = view.get_context_data()

        self.assertEqual("Create", context["action"])
        self.assertEqual(None, context["navigation"])

        # Navigation view = Foo
        view.navigation = "Foo"
        context = view.get_context_data()

        self.assertEqual("Foo", context["navigation"])

    def test_form_view(self):
        # No navigation view
        view = NavigationFormView()
        context = view.get_context_data()

        self.assertEqual(None, context["navigation"])

        # Navigation view = Foo
        view.navigation = "Foo"
        context = view.get_context_data()

        self.assertEqual("Foo", context["navigation"])

    def test_update_view(self):
        # No navigation view
        view = NavigationUpdateView()
        view.object = "blah"
        context = view.get_context_data()

        self.assertEqual("Update", context["action"])
        self.assertEqual(None, context["navigation"])

        # Navigation view = Foo
        view.navigation = "Foo"
        context = view.get_context_data()

        self.assertEqual("Foo", context["navigation"])
