# -*- coding: utf-8 -*-

import unittest

from board.core import app
from webtest import TestApp

# mock for response
TESTBOARD = "testboard"
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZjRkMzkxOTItZmFhZC00NDU4LThhNjktYzE0ZmJiZDQ0N2E0IiwibmFtZSI6IkFybm8gTnltb3VzIiwiYWRtaW4iOnRydWV9.S5pchdBRgdxk5Qk_SKgZQnuFQCNyGN5EHSDIxLPpirY"

test_app = TestApp(app)

id = 0


class response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_add_item(self):
        global id
        response = test_app.put('/board/' + TEST_TOKEN + '/' + TESTBOARD)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['name'], TESTBOARD)
        id = response.json['id']

    def test_list_all(self):
        response = test_app.get('/board/' + TEST_TOKEN )
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.content_type, "application/json")

    def test_delete_item(self):
        self.assertNotEqual(id, 0)
        response = test_app.delete('/board/' + TEST_TOKEN + '/' + str(id))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()
