# -*- coding: utf-8 -*-

from .context import board

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        board.hello()


if __name__ == '__main__':
    unittest.main()