import configparser
import hashlib
import json
import logging
import uuid

from bottle import Bottle, run, response, request, auth_basic, HTTPResponse
from jose import jwt

# read config file
config = configparser.ConfigParser()
config.read('config.ini')

# configure logging
logging.basicConfig(filename='board.log', level=logging.DEBUG)

app = Bottle()

user_list = []


@app.get('/')
def getinfo():
    return "<html><head><title>JAK-Login-Service</title></head><body>" \
           "<p>GET: <strong>/login</strong> Get Token</p>" \
           "<p>POST: <strong>/login</strong> Create user and get Token</p>" \
           "</body>"


def check(username, password):
    hashed_pw = hashlib.sha256(password.encode('utf-8'))
    check_user = [item for item in user_list if
                  item['username'] == username and item['password'] == hashed_pw.hexdigest()]
    return len(check_user) != 0


@app.get('/login')
@auth_basic(check)
def login():
    global user_list
    username = request.auth[0]
    user_item = [item for item in user_list if item['username'] == username]

    response.content_type = 'application/json; charset=utf-8'
    token = jwt.encode({
        'user_id': str(user_item['user_id'])
    }, config['jwt']['secret'], algorithm=config['jwt']['algorithm'])

    return json.dumps({
        'token': token
    })


@app.post('/login')
def create_login():
    global user_list
    username = request.forms.get('username')
    password = request.forms.get('password')
    user_id = uuid.uuid4()

    check_user = [item for item in user_list if item['username'] == username]

    if len(check_user) == 0:
        response.content_type = 'application/json; charset=utf-8'
        hashed = hashlib.sha256(password.encode('utf-8'))
        user_list.append({
            'user_id': str(user_id),
            'username': username,
            'password': hashed.hexdigest()
        })

        token = jwt.encode({'user_id': str(user_id)}, config['jwt']['secret'], algorithm=config['jwt']['algorithm'])
        return json.dumps({
            'token': token
        })
    return HTTPResponse(status=404)


# prevent running with nosetests
if __name__ == '__main__':
    logging.debug("Host: %s, Port: %s", config['login']['host'], config['login']['port'])
    run(app, host=config['login']['host'], port=config['login']['port'], debug=True, server='cherrypy')
