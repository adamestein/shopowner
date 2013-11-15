from django.utils import unittest

from test.inventory.models import HumanReadableModelTestCase
from test.inventory.navigation import NavigationTestCase
from test.inventory.loadpages import LoadPages

def suite():
    loader = unittest.TestLoader()

    hr = loader.loadTestsFromTestCase(HumanReadableModelTestCase)
    navigation = loader.loadTestsFromTestCase(NavigationTestCase)

    load_pages = loader.loadTestsFromTestCase(LoadPages)

    return unittest.TestSuite([hr, navigation, load_pages])

