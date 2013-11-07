from django.test import TestCase

from common.context_processors import version

class CPTestCase(TestCase):
    def test_version(self):
        ans = {
            "version": "Booth Apps v1.0"
        }

        self.assertEqual(version(None), ans)

