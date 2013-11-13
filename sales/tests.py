from django.utils import unittest

from test.sales.navigation import NavigationTestCase

def suite():
    suite_navigation = unittest.TestLoader().loadTestsFromTestCase(NavigationTestCase)

    return unittest.TestSuite([suite_navigation])

