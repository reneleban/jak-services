# -*- coding: utf-8 -*-
"""
.. module:: login
    :platform: osx, linux
    :synopsis: LOGIN Rest Microservice for JAK
.. moduleauthor:: René Leban<leban.rene@gmail.com>
"""
import configparser
import hashlib
import json
import logging
import uuid
import dataset

from bottle import Bottle, run, response, request, auth_basic, HTTPResponse
from jose import jwt

# read config file
CONFIG = configparser.ConfigParser()
CONFIG.read('login.ini')

# configure logging
logging.basicConfig(filename=CONFIG['login']['logfile'], level=logging.DEBUG)

SQLITE_CONNECTION = CONFIG['login']['sqlite_connect']

APP = Bottle()


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method='GET', callback=self._index)

    def _index():
        """
            Info message about implemented Operations
            :return: Simple HTML with some information's
            """
        return "<html><head><title>JAK-Login-Service</title></head><body>" \
               "<p>GET: <strong>/login</strong> Get Token</p>" \
               "<p>POST: <strong>/login</strong> Create user and get Token</p>" \
               "<p>DELETE: <strong>/login</strong> Delete User</p>" \
               "</body>"

    def _check(username, password):
        """
        authentication check used for basic auth
        :param username: user to log in
        :param password: password for log in
        :return: boolean
        """
        logging.info("checking credentials for: %s", username)
        hashed_pw = hashlib.sha256(password.encode('utf-8'))
        result = False

        with dataset.connect(SQLITE_CONNECTION) as login_db:
            user_table = login_db['users']
            check_user = user_table.find_one(username=username)

        if check_user is not None:
            result = check_user['password'] == hashed_pw.hexdigest()

        return result

    @APP.delete('/login')
    @auth_basic(check)
    def _remove_login():
        """
        delete user, authentication using auth basic
        :return: 200 if ok, 404 on error
        """
        username = request.auth[0]

        with dataset.connect(SQLITE_CONNECTION) as login_db:
            login_db.begin()
            try:
                user_table = login_db['users']
                user_table.delete(username=username)
                login_db.commit()
                return HTTPResponse(status=200)
            except:
                login_db.rollback()
                return HTTPResponse(status=404)

server = Server(host=CONFIG['login']['host'], port=CONFIG['login']['port'])
server.start()

@APP.get('/')
def getinfo():
    """
    Info message about implemented Operations
    :return: Simple HTML with some information's
    """
    return "<html><head><title>JAK-Login-Service</title></head><body>" \
           "<p>GET: <strong>/login</strong> Get Token</p>" \
           "<p>POST: <strong>/login</strong> Create user and get Token</p>" \
           "<p>DELETE: <strong>/login</strong> Delete User</p>" \
           "</body>"


def check(username, password):
    """
    authentication check used for basic auth
    :param username: user to log in
    :param password: password for log in
    :return: boolean
    """
    logging.info("checking credentials for: %s", username)
    hashed_pw = hashlib.sha256(password.encode('utf-8'))
    result = False

    with dataset.connect(SQLITE_CONNECTION) as login_db:
        user_table = login_db['users']
        check_user = user_table.find_one(username=username)

    if check_user is not None:
        result = check_user['password'] == hashed_pw.hexdigest()

    return result


@APP.delete('/login')
@auth_basic(check)
def remove_login():
    """
    delete user, authentication using auth basic
    :return: 200 if ok, 404 on error
    """
    username = request.auth[0]

    with dataset.connect(SQLITE_CONNECTION) as login_db:
        login_db.begin()
        try:
            user_table = login_db['users']
            user_table.delete(username=username)
            login_db.commit()
            return HTTPResponse(status=200)
        except:
            login_db.rollback()
            return HTTPResponse(status=404)


@APP.get('/login')
@auth_basic(check)
def login():
    """
    login user using auth_basic
    :return: 200 and JSON String with token or HTTPStatus 404 on error
    """
    username = request.auth[0]
    with dataset.connect(SQLITE_CONNECTION) as login_db:
        try:
            user_table = login_db['users']
            user = user_table.find_one(username=username)
            logging.debug("generating token for user %s", user['user_id'])
            response.content_type = 'application/json; charset=utf-8'
            token = jwt.encode({
                'user_id': str(user['user_id'])
            }, CONFIG['jwt']['secret'], algorithm=CONFIG['jwt']['algorithm'])
            return json.dumps({
                'token': token
            })
        except:
            return HTTPResponse(status=404)


@APP.get('/login/validate/<token>')
def validate(token):
    """
    check for valid token, used for stored tokens on devices
    :param token: token to check
    :return: Status 200 if ok, 404 on error.
    """
    with dataset.connect(SQLITE_CONNECTION) as login_db:
        login_db.begin()
        try:
            user_data = jwt.decode(token,
                                   CONFIG['jwt']['secret'],
                                   algorithms=[CONFIG['jwt']['algorithm']])
            user = login_db['users'].find_one(user_id=user_data['user_id'])
            if user is None:
                return HTTPResponse(status=404)
            else:
                return HTTPResponse(status=200)
        except:
            return HTTPResponse(status=404)


@APP.post('/login')
def create_login():
    """
    create new user login
    :return: 409 if user already exists, 404 on error, 200 and JSON String with token on success
    """
    forms = request.forms
    username = forms.username
    password = forms.password
    user_id = uuid.uuid4()
    logging.info("processing create_login for given username: %s", username)
    logging.debug("checking for existence: %s", username)

    with dataset.connect(SQLITE_CONNECTION) as login_db:
        user_table = login_db['users']
        check_user = user_table.find_one(username=username)

    if check_user is None:
        response.content_type = 'application/json; charset=utf-8'
        hashed = hashlib.sha256(password.encode('utf-8'))
        new_user = {
            'user_id': str(user_id),
            'username': username,
            'password': hashed.hexdigest()
        }

        logging.debug("insert user to sqlite-db %s", SQLITE_CONNECTION)

        with dataset.connect(SQLITE_CONNECTION) as login_db:
            login_db.begin()
            try:
                logging.debug("appending %s to user_table", new_user)
                user_table = login_db['users']
                user_table.insert(new_user)
                login_db.commit()
                token = jwt.encode({'user_id': str(user_id)}, CONFIG['jwt']['secret'],
                                   algorithm=CONFIG['jwt']['algorithm'])
                return json.dumps({
                    'token': token
                })
            except:
                login_db.rollback()
                return HTTPResponse(status=404)
    else:
        return HTTPResponse(status=409)  # conflict


# prevent running with nosetests
if __name__ == '__main__':
    logging.debug("Host: %s, Port: %s", CONFIG['login']['host'], CONFIG['login']['port'])
    run(APP,
        host=CONFIG['login']['host'],
        port=CONFIG['login']['port'],
        debug=True,
        server='cherrypy')
