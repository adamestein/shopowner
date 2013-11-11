from django.utils import unittest

from test.inventory.models import HumanReadableModelTestCase
from test.inventory.navigation import NavigationTestCase

def suite():
    suite_hr = unittest.TestLoader().loadTestsFromTestCase(HumanReadableModelTestCase)
    suite_navigation = unittest.TestLoader().loadTestsFromTestCase(NavigationTestCase)

    return unittest.TestSuite([suite_hr, suite_navigation])

