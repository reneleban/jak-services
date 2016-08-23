import configparser
import hashlib
import json
import logging
import uuid
import dataset

from bottle import Bottle, run, response, request, auth_basic, HTTPResponse
from jose import jwt

# read config file
config = configparser.ConfigParser()
config.read('login.ini')

# configure logging
logging.basicConfig(filename=config['login']['logfile'], level=logging.DEBUG)

SQLITE_CONNECTION = config['login']['sqlite_connect']

app = Bottle()


@app.get('/')
def getinfo():
    return "<html><head><title>JAK-Login-Service</title></head><body>" \
           "<p>GET: <strong>/login</strong> Get Token</p>" \
           "<p>POST: <strong>/login</strong> Create user and get Token</p>" \
           "<p>DELETE: <strong>/login</strong> Delete User</p>" \
           "</body>"


def check(username, password):
    logging.info("checking credentials for: %s", username)
    hashed_pw = hashlib.sha256(password.encode('utf-8'))
    hashed_pw = hashed_pw.hexdigest()

    result = False
    login_db = dataset.connect(SQLITE_CONNECTION)

    user_table = login_db['users']
    check_user = user_table.find_one(username=username)
    if check_user is not None:
        result = check_user['password'] == hashed_pw

    return result


@app.delete('/login')
@auth_basic(check)
def remove_login():
    username = request.auth[0]

    login_db = dataset.connect(SQLITE_CONNECTION)
    user_table = login_db['users']
    user_table.delete(username=username)

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({
        'message': username + ' deleted'
    })


@app.get('/login')
@auth_basic(check)
def login():
    username = request.auth[0]
    login_db = dataset.connect(SQLITE_CONNECTION)
    user_table = login_db['users']
    user = user_table.find_one(username=username)

    logging.debug("generating token for user %s", user['user_id'])
    response.content_type = 'application/json; charset=utf-8'
    token = jwt.encode({
        'user_id': str(user['user_id'])
    }, config['jwt']['secret'], algorithm=config['jwt']['algorithm'])

    return json.dumps({
        'token': token
    })


@app.post('/login')
def create_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    user_id = uuid.uuid4()
    logging.info("processing create_login for given username: %s", username)
    logging.debug("checking for existence: %s", username)

    login_db = dataset.connect(SQLITE_CONNECTION)
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

        user_table.insert(new_user)

        logging.debug("appending %s to user_table", new_user)

        token = jwt.encode({'user_id': str(user_id)}, config['jwt']['secret'], algorithm=config['jwt']['algorithm'])
        return json.dumps({
            'token': token
        })
    return HTTPResponse(status=404)


# prevent running with nosetests
if __name__ == '__main__':
    logging.debug("Host: %s, Port: %s", config['login']['host'], config['login']['port'])
    run(app, host=config['login']['host'], port=config['login']['port'], debug=True, server='cherrypy')
