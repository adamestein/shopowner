from django.utils import unittest

from test.common.cp import CPTestCase
from test.common.views.generic import BaseViewsTestCase
from test.common.navigation import NavigationTestCase

def suite():
    suite_cp = unittest.TestLoader().loadTestsFromTestCase(CPTestCase)
    suite_base_views = unittest.TestLoader().loadTestsFromTestCase(BaseViewsTestCase)
    suite_navigation = unittest.TestLoader().loadTestsFromTestCase(NavigationTestCase)

    return unittest.TestSuite([suite_cp, suite_base_views, suite_navigation])

