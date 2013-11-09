from django.test import TestCase

from common.navigation import Navigation

class NavigationTestCase(TestCase):
    def test_Navigation(self):
        # No subject
        ans = (
            ["Inventory", "/shopowner/inventory/"],
            ["Sales", "/shopowner/sales/"],
        )

        self.assertEqual(Navigation(""), ans)

