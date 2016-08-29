# -*- coding: utf-8 -*-

import unittest
import uuid

from webtest import TestApp

from src.card.core import app

# mock for response
TEST_CARD_NAME = "testcard"
TEST_CARD_DESC = "testdescription"
TEST_LIST_ID = str(uuid.uuid4())
TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmJhNDNjM2MtNmMzYS00OTRiLThi" \
             "MGYtZTUyYWJmMjJjYjNjIn0.271QJQDYQJWPSg0vDsQziUYI7e1YSDS4zpc6HibZUYk"

test_app = TestApp(app)


ID = 0


class Response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_add_item(self):
        global ID
        response = test_app.put('/cards/'
                                + TEST_TOKEN + '/'
                                + TEST_LIST_ID, {
            "name": TEST_CARD_NAME,
            "description": TEST_CARD_DESC
        })
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['name'], TEST_CARD_NAME)
        self.assertEqual(response.json['list_id'], TEST_LIST_ID)
        ID = response.json['card_id']

    def test_list_contains_card(self):
        response = test_app.get('/cards/' + TEST_TOKEN + '/' + TEST_LIST_ID)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json[0]['name'], TEST_CARD_NAME)
        self.assertEqual(response.json[0]['description'], TEST_CARD_DESC)
        self.assertEqual(response.json[0]['card_id'], ID)

    def test_remove_card(self):
        response = test_app.delete('/cards/' + TEST_TOKEN + '/' + str(ID))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['deleted'], True)


if __name__ == '__main__':
    unittest.main()
