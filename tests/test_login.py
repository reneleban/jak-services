import unittest

from login.core import app
from webtest import TestApp

test_app = TestApp(app)

token = ""


class response:
    content_type = ""


class TestJSON(unittest.TestCase):

    def test_create_login(self):
        global token
        response = test_app.post('/login', {
            "username": "user",
            "password": "pass"
        })
        self.assertEqual(response.status_int, 200)
        token = response.json['token']

    def test_delete(self):
        global token
        test_app.authorization = ('Basic', ('user', 'pass'))
        response = test_app.delete('/login')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.json["message"], "user deleted")

if __name__ == '__main__':
    unittest.main()
