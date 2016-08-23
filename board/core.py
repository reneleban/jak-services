# -*- coding: utf-8 -*-
import configparser
import json
import logging
import os
import uuid
import dataset

from bottle import Bottle, run, response, HTTPResponse
from jose import jwt

# read config file
config = configparser.ConfigParser()
config.read('config.ini')

# configure logging
logging.basicConfig(filename=config['board']['logfile'], level=logging.DEBUG)

SQLITE_CONNECTION = config['board']['sqlite_connect']

app = Bottle()


@app.get('/')
def getinfo():
    return "<html><head><title>JAK-Board-Service</title></head><body>" \
           "<p>GET: <strong>/board/token</strong> - list all boards</p>" \
           "<p>PUT: <strong>/board/[a-z]/token</strong> - add board</p>" \
           "<p>DELETE: <strong>/board/[0-9]/token</strong> - delete by ID</p>" \
           "</body></html>"


@app.get('/board/<token>')
def getrequest(token):
    logging.debug('token: ' + token)
    userdata = jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])
    logging.debug('list all boards for user: ' + userdata["user_id"])
    return list_all_boards(userdata['user_id'], response)


@app.put('/board/<token>/<name:re:[a-zA-Z\s]*>')
def postrequest(name, token):
    logging.debug('token: ' + token)
    userdata = jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])
    return addboard(userdata['user_id'], response, name)


@app.delete('/board/<token>/<board_id>')
def deletebyidrequest(board_id, token):
    logging.debug('token: ' + token)
    userdata = jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])
    return removeboard(userdata['user_id'], response, board_id)


def list_all_boards(user_uuid, response):
    response.content_type = 'application/json; charset=utf-8'
    board_db = dataset.connect(SQLITE_CONNECTION)
    # SELECT * FROM boards INNER JOIN acl USING (board_id) WHERE acl.user_id=user_uuid
    result = board_db.query("SELECT board_id, name FROM boards INNER JOIN acl USING (board_id) where acl.user_id='" +
                            user_uuid + "'")
    dict_result = []
    for row in result:
        dict_result.append({
            'board_id': row['board_id'],
            'name': row['name']
        })

    return json.dumps(dict_result)


def addboard(user_uuid, response, name):
    board_uuid = uuid.uuid4()

    new_board = {'board_id': str(board_uuid), 'name': name}
    new_acl = {'board_id': str(board_uuid), 'user_id': str(user_uuid)}

    board_db = dataset.connect(SQLITE_CONNECTION)
    board_db['boards'].insert(new_board)
    board_db['acl'].insert(new_acl)

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(new_board)


def removeboard(user_uuid, response, board_id):
    board_db = dataset.connect(SQLITE_CONNECTION)
    acl_table = board_db['acl']
    board_tbl = board_db['boards']

    acl = acl_table.find_one(user_id=user_uuid, board_id=board_id)
    if acl is not None:
        acl_table.delete(board_id=board_id)
        board_tbl.delete(board_id=board_id)
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({'message': board_id + ' deleted'})
    else:
        return HTTPResponse(status=404)


# prevent running with nosetests
if __name__ == '__main__':
    run(app, host=config['board']['host'], port=config['board']['port'], debug=True, server='cherrypy')
