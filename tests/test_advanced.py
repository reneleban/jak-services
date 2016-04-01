# -*- coding: utf-8 -*-

from .context import board

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        assert board.hello() == "Hello Wurst!"

    def test_getrequest(self):
        assert board.getrequest() == "[1, true, 3, {\"6\": 7, \"4\": 5}]"

    def test_postrequest(self):
        assert board.postrequest() == "POST"


if __name__ == '__main__':
    unittest.main()