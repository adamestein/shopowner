from django.utils import unittest

from test.common.cp import CPTestCase
from test.common.format import FormatTestCase
from test.common.navigation import NavigationTestCase
from test.common.views.generic import BaseViewsTestCase, EditViewsTestCase, ListViewsTestCase

def suite():
    suite_cp = unittest.TestLoader().loadTestsFromTestCase(CPTestCase)
    suite_base_views = unittest.TestLoader().loadTestsFromTestCase(BaseViewsTestCase)
    suite_edit_views = unittest.TestLoader().loadTestsFromTestCase(EditViewsTestCase)
    suite_format = unittest.TestLoader().loadTestsFromTestCase(FormatTestCase)
    suite_list_views = unittest.TestLoader().loadTestsFromTestCase(ListViewsTestCase)
    suite_navigation = unittest.TestLoader().loadTestsFromTestCase(NavigationTestCase)

    return unittest.TestSuite([
        suite_cp, suite_base_views, suite_edit_views, suite_format, suite_list_views, suite_navigation
    ])

