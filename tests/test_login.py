import unittest

from webtest import TestApp

from src.login.core import APP

test_app = TestApp(APP)

TOKEN = ""


class TestJSON(unittest.TestCase):

    def test_create_login(self):
        global TOKEN
        response = test_app.post('/login', {
            "username": "user",
            "password": "pass"
        })
        self.assertEqual(response.status_int, 200)
        TOKEN = response.json['token']

    def test_do_validate_valid_token(self):
        global TOKEN
        response = test_app.get('/login/validate/'+TOKEN)
        self.assertEqual(response.status_int, 200)

    def test_do_validate_illegal_token(self):
        response = test_app.get('/login/validate/invalid', status=404)
        self.assertEqual(response.status_int, 404)

    def test_user_delete(self):
        global TOKEN
        test_app.authorization = ('Basic', ('user', 'pass'))
        resp = test_app.delete('/login')
        self.assertEqual(resp.status_int, 200)

if __name__ == '__main__':
    unittest.main()
