from django.utils import unittest

from test.sales.loadpages import LoadPages
from test.sales.models import HumanReadableModelTestCase
from test.sales.navigation import NavigationTestCase

def suite():
    loader = unittest.TestLoader()

    hr = loader.loadTestsFromTestCase(HumanReadableModelTestCase)
    navigation = loader.loadTestsFromTestCase(NavigationTestCase)

    load_pages = loader.loadTestsFromTestCase(LoadPages)

    return unittest.TestSuite([hr, navigation, load_pages])

