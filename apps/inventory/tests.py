from django.utils import unittest

from test.inventory.forms import FormsTestCase
from test.inventory.loadpages import LoadPages
from test.inventory.models import HumanReadableModelTestCase
from test.inventory.navigation import NavigationTestCase
from test.inventory.nolist import NoList

def suite():
    loader = unittest.TestLoader()

    hr = loader.loadTestsFromTestCase(HumanReadableModelTestCase)
    navigation = loader.loadTestsFromTestCase(NavigationTestCase)

    load_pages = loader.loadTestsFromTestCase(LoadPages)
    no_list = loader.loadTestsFromTestCase(NoList)
    forms = loader.loadTestsFromTestCase(FormsTestCase)

    return unittest.TestSuite([hr, navigation, load_pages, no_list, forms])

