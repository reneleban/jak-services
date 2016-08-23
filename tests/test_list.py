# -*- coding: utf-8 -*-

import unittest
import uuid

from list.core import app
from webtest import TestApp

# mock for response
TESTLIST = "testlist"
TEST_BOARD_ID = str(uuid.uuid4())
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZjRkMzkxOTItZmFhZC00NDU4LThhNjktYzE0ZmJiZDQ0N2E0IiwibmFtZSI6IkFybm8gTnltb3VzIiwiYWRtaW4iOnRydWV9.S5pchdBRgdxk5Qk_SKgZQnuFQCNyGN5EHSDIxLPpirY"

test_app = TestApp(app)


id = 0

class response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_add_item(self):
        global id
        response = test_app.put('/lists/board/' + TEST_TOKEN + '/' + TEST_BOARD_ID + '/' + TESTLIST)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['name'], TESTLIST)
        self.assertEqual(response.json['board_id'], TEST_BOARD_ID)
        id = response.json['list_id']

    def test_board_contains_list(self):
        response = test_app.get('/lists/list/' + TEST_TOKEN + '/' + TEST_BOARD_ID)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json[0]['name'], TESTLIST)
        self.assertEqual(response.json[0]['list_id'], id)

    def test_board_remove_list(self):
        response = test_app.delete('/lists/list/' + TEST_TOKEN + '/' + str(id))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['deleted'], True)


if __name__ == '__main__':
    unittest.main()
