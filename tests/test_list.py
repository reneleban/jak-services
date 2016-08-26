# -*- coding: utf-8 -*-

import unittest
import uuid

from webtest import TestApp

from src.list import app

# mock for response
TESTLIST = "testlist"
TEST_BOARD_ID = str(uuid.uuid4())
TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmJhNDNjM2MtNmMzYS00OTRiLThi" \
             "MGYtZTUyYWJmMjJjYjNjIn0.271QJQDYQJWPSg0vDsQziUYI7e1YSDS4zpc6HibZUYk"

test_app = TestApp(app)


ID = 0


class Response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_add_item(self):
        global ID
        response = test_app.put('/lists/board/' + TEST_TOKEN + '/' + TEST_BOARD_ID + '/' + TESTLIST)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['name'], TESTLIST)
        self.assertEqual(response.json['board_id'], TEST_BOARD_ID)
        ID = response.json['list_id']

    def test_board_contains_list(self):
        response = test_app.get('/lists/list/' + TEST_TOKEN + '/' + TEST_BOARD_ID)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json[0]['name'], TESTLIST)
        self.assertEqual(response.json[0]['list_id'], ID)

    def test_board_remove_list(self):
        response = test_app.delete('/lists/list/' + TEST_TOKEN + '/' + str(ID))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['deleted'], True)


if __name__ == '__main__':
    unittest.main()
