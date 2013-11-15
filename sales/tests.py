from django.utils import unittest

from test.sales.loadpages import LoadPages
from test.sales.navigation import NavigationTestCase

def suite():
    loader = unittest.TestLoader()

    navigation = loader.loadTestsFromTestCase(NavigationTestCase)
    load_pages = loader.loadTestsFromTestCase(LoadPages)

    return unittest.TestSuite([navigation, load_pages])

