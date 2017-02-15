#!/user/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time

from test_base import BaseTest


class IndexTest(BaseTest):
    # 打开首页
    def test_index_open(self):
        self.browser.get("http://localhost:5000/")
        self.assertIn(u"友联亿思", self.browser.title, "打开首页失败")
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
