#!/user/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time
from selenium import webdriver


# Selenium测试基本类
class BaseTest(unittest.TestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.browser = webdriver.Chrome()
        except Exception as e:
            print e

    def setUp(self):

        if not self.browser:
            self.skipTest('web browser not availble')
        self.browser.set_window_size(1600, 1200)

    def tearDown(self):
        time.sleep(10)
        self.browser.quit()
