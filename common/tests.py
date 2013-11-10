from django.utils import unittest

from test.common.cp import CPTestCase
from test.common.format import FormatTestCase
from test.common.navigation import NavigationTestCase
from test.common.views.generic import BaseViewsTestCase

def suite():
    suite_cp = unittest.TestLoader().loadTestsFromTestCase(CPTestCase)
    suite_base_views = unittest.TestLoader().loadTestsFromTestCase(BaseViewsTestCase)
    suite_format = unittest.TestLoader().loadTestsFromTestCase(FormatTestCase)
    suite_navigation = unittest.TestLoader().loadTestsFromTestCase(NavigationTestCase)

    return unittest.TestSuite([suite_cp, suite_base_views, suite_format, suite_navigation])

