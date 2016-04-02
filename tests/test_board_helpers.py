# -*- coding: utf-8 -*-

from .context import board
import unittest


# mock for response
class response:
    content_type = ""


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_add_board(self):
        resp = response()
        result = board.addboard(response=resp, name="testboard")
        assert "testboard" in result
        assert "application/json" in resp.content_type

    def test_list_boards(self):
        resp = response();
        result = board.listallboards(response=resp)
        assert "testboard" in result
        assert "application/json" in resp.content_type

    def test_remove_board(self):
        resp = response()
        id = 1
        result = board.removeboard(resp, id)
        assert "true" in result
        assert "application/json" in resp.content_type


if __name__ == '__main__':
    unittest.main()
