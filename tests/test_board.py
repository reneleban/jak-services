# -*- coding: utf-8 -*-

import unittest

from board.core import app
from webtest import TestApp

# mock for response
TESTBOARD = "testboard"

test_app = TestApp(app)

id = 0


class response:
    content_type = ""


class TestJSON(unittest.TestCase):
    def test_list_all(self):
        response = test_app.get('/board')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.content_type, "application/json")

    def test_add_item(self):
        global id
        response = test_app.put('/board/' + TESTBOARD)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json['name'], TESTBOARD)
        id = response.json['id']

    def test_list_all_with_trailing(self):
        response = test_app.get('/board/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.content_type, "application/json")

    def test_delete_item(self):
        self.assertNotEqual(id, 0)
        response = test_app.delete('/board/' + str(id))
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()
