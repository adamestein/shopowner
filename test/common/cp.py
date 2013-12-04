from django.test import TestCase

from common.context_processors import version

class CPTestCase(TestCase):
    def test_version(self):
        ans = {
            "version": "Shop Owner Apps v1.1"
        }

        self.assertEqual(version(None), ans)

