# -*- coding: utf-8 -*-

import unittest

from list.core import app
from webtest import TestApp

# mock for response
TESTLIST = "testlist"
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZjRkMzkxOTItZmFhZC00NDU4LThhNjktYzE0ZmJiZDQ0N2E0IiwibmFtZSI6IkFybm8gTnltb3VzIiwiYWRtaW4iOnRydWV9.S5pchdBRgdxk5Qk_SKgZQnuFQCNyGN5EHSDIxLPpirY"

test_app = TestApp(app)

class response:
    content_type = ""


# class TestJSON(unittest.TestCase):

    # def test_add_list(self):
    #     resp = response()
    #     board_id = 0
    #     result = list.add_list(response=resp, board_id=board_id, name=TESTLIST)
    #     assert TESTLIST in result
    #     assert "application/json" in resp.content_type
    #
    # def test_lists_for_board(self):
    #     resp = response()
    #     board_id = 0
    #     result = list.lists_for_board(response=resp, board_id=board_id)
    #     assert TESTLIST in result
    #     assert "application/json" in resp.content_type
    #
    # def test_remove_list(self):
    #     resp = response()
    #     list_id = 1
    #     result = list.remove_list(response=resp, list_id=list_id)
    #     assert "true" in result
    #     assert "application/json" in resp.content_type
    #
    # def test_add_and_delete_for_board(self):
    #     resp = response()
    #     board_id = 0
    #     result = list.add_list(response=resp, board_id=board_id, name=TESTLIST)
    #     assert TESTLIST in result
    #     assert "application/json" in resp.content_type
    #     list.add_list(response=resp, board_id=board_id, name='TESTLIST1')
    #     lists = list.lists_for_board(response=resp, board_id=board_id)
    #     assert TESTLIST in lists
    #     assert 'TESTLIST1' in lists
    #     result = list.remove_list(response=resp, list_id=2)
    #     assert "true" in result
    #     result = list.remove_lists_for_board(response=resp, board_id=board_id)
    #     assert "true" in result


if __name__ == '__main__':
    unittest.main()
