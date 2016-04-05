# -*- coding: utf-8 -*-

from .context import board
import unittest


# mock for response
TESTBOARD = "testboard"


class response:
    content_type = ""


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_add_board(self):
        resp = response()
        result = board.addboard(response=resp, name=TESTBOARD)
        assert TESTBOARD in result
        assert "application/json" in resp.content_type

    def test_list_boards(self):
        resp = response()
        result = board.listallboards(response=resp)
        assert TESTBOARD in result
        assert "application/json" in resp.content_type

    def test_remove_board(self):
        resp = response()
        id = 1
        result = board.removeboard(resp, id)
        assert "true" in result
        assert "application/json" in resp.content_type

    def test_add_and_delete_by_name_board(self):
        resp = response()
        result = board.addboard(response=resp, name=TESTBOARD)
        assert TESTBOARD in result
        assert "application/json" in resp.content_type
        result = board.removeboardbyname(resp, TESTBOARD)
        assert "true" in result
        assert "application/json" in resp.content_type


if __name__ == '__main__':
    unittest.main()
