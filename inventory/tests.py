from django.utils import unittest

from test.inventory.models import HumanReadableModelTestCase

def suite():
    suite_hr = unittest.TestLoader().loadTestsFromTestCase(HumanReadableModelTestCase)

    return unittest.TestSuite([suite_hr])

