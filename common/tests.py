from django.utils import unittest

from test.common.cp import CPTestCase
from test.common.format import FormatTestCase
from test.common.views.generic import BaseViewsTestCase, EditViewsTestCase, ListViewsTestCase
from test.common.forms import WidgetsTestCase

def suite():
    loader = unittest.TestLoader()

    cp = loader.loadTestsFromTestCase(CPTestCase)
    base_views = loader.loadTestsFromTestCase(BaseViewsTestCase)
    edit_views = loader.loadTestsFromTestCase(EditViewsTestCase)
    fmt = loader.loadTestsFromTestCase(FormatTestCase)
    list_views = loader.loadTestsFromTestCase(ListViewsTestCase)
    widgets = loader.loadTestsFromTestCase(WidgetsTestCase)

    return unittest.TestSuite([
        cp, base_views, edit_views, fmt, list_views, widgets
    ])

