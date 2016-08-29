# -*- coding: utf-8 -*-

import unittest
import urllib.parse

from webtest import TestApp

from src.board.core import APP

# mock for response
TEST_BOARD = "testboard üsing söme ;specials"
TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmJhNDNjM2MtNmMzYS00OTRiLThi" \
             "MGYtZTUyYWJmMjJjYjNjIn0.271QJQDYQJWPSg0vDsQziUYI7e1YSDS4zpc6HibZUYk"

test_app = TestApp(APP)

ID = 0


class TestJSON(unittest.TestCase):

    def test_add_item(self):
        global ID
        res = test_app.put('/board/' + TEST_TOKEN, params={
            'name': TEST_BOARD
        }, headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        })
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, "application/json")
        self.assertEqual(res.json['name'], TEST_BOARD)
        ID = res.json['board_id']

    def test_list_all(self):
        res = test_app.get('/board/' + TEST_TOKEN)
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.status, "200 OK")
        self.assertEqual(res.content_type, "application/json")

    def test_delete_item(self):
        self.assertNotEqual(ID, 0)
        res = test_app.delete('/board/' + TEST_TOKEN + '/' + str(ID))
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()
