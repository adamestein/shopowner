#!/usr/bin/python

from selenium import webdriver
import unittest

class MainPageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    #def tearDown(self):
    #    self.browser.quit()

    def test_mainpage(self):
        self.browser.get("http://localhost:8000/shopowner/")

        self.assertEqual("Shop Owner Applications", self.browser.title)

if __name__ == "__main__":
    unittest.main()

