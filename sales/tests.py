from django.utils import unittest

from test.sales.loadpages import LoadPages
from test.sales.models import HumanReadableModelTestCase
from test.sales.navigation import NavigationTestCase
from test.sales.utils import UtilsTestCase

def suite():
    loader = unittest.TestLoader()

    hr = loader.loadTestsFromTestCase(HumanReadableModelTestCase)
    navigation = loader.loadTestsFromTestCase(NavigationTestCase)
    utils = loader.loadTestsFromTestCase(UtilsTestCase)

    load_pages = loader.loadTestsFromTestCase(LoadPages)

    return unittest.TestSuite([hr, navigation, utils, load_pages])

