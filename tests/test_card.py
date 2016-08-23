# -*- coding: utf-8 -*-

import unittest
import uuid

from card.core import app
from webtest import TestApp

# mock for response
TEST_CARD_TITLE = "testcard"
TEST_CARD_DESC = "testdescription"
TEST_LIST_ID = str(uuid.uuid4())
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZjRkMzkxOTItZmFhZC00NDU4LThhNjktYzE0ZmJiZDQ0N2E0IiwibmFtZSI6IkFybm8gTnltb3VzIiwiYWRtaW4iOnRydWV9.S5pchdBRgdxk5Qk_SKgZQnuFQCNyGN5EHSDIxLPpirY"

test_app = TestApp(app)


id = 0

class response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_add_item(self):
        global id
        response = test_app.put('/cards/' + TEST_TOKEN + '/' + TEST_LIST_ID + '/' + TEST_CARD_TITLE + '/' + TEST_CARD_DESC)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['name'], TEST_CARD_TITLE)
        self.assertEqual(response.json['list_id'], TEST_LIST_ID)
        id = response.json['card_id']

    def test_list_contains_card(self):
        response = test_app.get('/cards/' + TEST_TOKEN + '/' + TEST_LIST_ID)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json[0]['name'], TEST_CARD_TITLE)
        self.assertEqual(response.json[0]['description'], TEST_CARD_DESC)
        self.assertEqual(response.json[0]['card_id'], id)

    def test_remove_card(self):
        response = test_app.delete('/cards/' + TEST_TOKEN + '/' + str(id))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['deleted'], True)


if __name__ == '__main__':
    unittest.main()