import unittest

from webtest import TestApp

from src.login.core import APP

test_app = TestApp(APP)

TOKEN = ""


class Response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_create_login(self):
        global TOKEN
        response = test_app.post('/login', {
            "username": "user",
            "password": "pass"
        })
        self.assertEqual(response.status_int, 200)
        TOKEN = response.json['token']

    def test_delete(self):
        global TOKEN
        test_app.authorization = ('Basic', ('user', 'pass'))
        resp = test_app.delete('/login')
        self.assertEqual(resp.status_int, 200)

if __name__ == '__main__':
    unittest.main()
