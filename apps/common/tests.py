import unittest

from test.common.format import FormatTestCase
from test.common.views.generic import BaseViewsTestCase, EditViewsTestCase, ListViewsTestCase
from test.common.forms import WidgetsTestCase


def suite():
    loader = unittest.TestLoader()

    base_views = loader.loadTestsFromTestCase(BaseViewsTestCase)
    edit_views = loader.loadTestsFromTestCase(EditViewsTestCase)
    fmt = loader.loadTestsFromTestCase(FormatTestCase)
    list_views = loader.loadTestsFromTestCase(ListViewsTestCase)
    widgets = loader.loadTestsFromTestCase(WidgetsTestCase)

    return unittest.TestSuite([
        base_views, edit_views, fmt, list_views, widgets
    ])

