# -*- coding: utf-8 -*-
"""
    BOARD Rest-Microservice for JAK

    Implemented: get, put, delete
"""

import configparser
import json
import logging
import uuid
import dataset

from bottle import Bottle, run, response, HTTPResponse
from jose import jwt

# read config file
CONFIG = configparser.ConfigParser()
CONFIG.read('board.ini')

# configure logging
logging.basicConfig(filename=CONFIG['board']['logfile'], level=logging.DEBUG)

SQLITE_CONNECTION = CONFIG['board']['sqlite_connect']

APP = Bottle()


@APP.get('/')
def getinfo():
    """
    Info message about implemented Operations
    :return: Simple HTML with some information's
    """
    return "<html><head><title>JAK-Board-Service</title></head><body>" \
           "<p>GET: <strong>/board/token</strong> - list all boards</p>" \
           "<p>PUT: <strong>/board/[a-z]/token</strong> - add board</p>" \
           "<p>DELETE: <strong>/board/[0-9]/token</strong> - delete by ID</p>" \
           "</body></html>"


@APP.get('/board/<token>')
def list_all_boards(token):
    """
    Request all boards for user with given token
    :param token: user token
    :return: JSON-Board List or HTTPStatus 404
    """
    board_list = []
    user_data = jwt.decode(token, CONFIG['jwt']['secret'], algorithms=[CONFIG['jwt']['algorithm']])
    logging.debug('list all boards for user: ' + user_data["user_id"])
    with dataset.connect(SQLITE_CONNECTION) as board_db:
        try:
            result = board_db.query("SELECT board_id, name FROM boards INNER JOIN acl "
                                    "USING (board_id) "
                                    "where acl.user_id='" + user_data["user_id"] + "'")
            for row in result:
                board_list.append({
                    'board_id': row['board_id'],
                    'name': row['name']
                })
            response.content_type = 'application/json; charset=utf-8'
            return json.dumps(board_list)
        except:
            return HTTPResponse(status=404)


@APP.put('/board/<token>/<name>')
def add_board(name, token):
    """
    Insert new Board with given 'name' for user 'token'
    :param name: new boards name
    :param token: user token
    :return: JSON with board_id and name or HTTPStatus 404
    """
    user_data = jwt.decode(token, CONFIG['jwt']['secret'], algorithms=[CONFIG['jwt']['algorithm']])
    board_uuid = uuid.uuid4()
    new_board = {'board_id': str(board_uuid), 'name': name}
    new_acl = {'board_id': str(board_uuid), 'user_id': str(user_data['user_id'])}

    with dataset.connect(SQLITE_CONNECTION) as board_db:
        board_db.begin()
        try:
            board_db['boards'].insert(new_board)
            board_db['acl'].insert(new_acl)
            board_db.commit()
            response.content_type = 'application/json; charset=utf-8'
            return json.dumps(new_board)
        except:
            board_db.rollback()
            return HTTPResponse(status=404)


@APP.delete('/board/<token>/<board_id>')
def remove_board(board_id, token):
    """
    Remove board 'board_id' with user 'token'
    :param board_id: board_id to remove
    :param token: user token
    :return: 200 an JSON Message OK or 404 on Exception or ACL Error
    """
    user_data = jwt.decode(token, CONFIG['jwt']['secret'], algorithms=[CONFIG['jwt']['algorithm']])

    with dataset.connect(SQLITE_CONNECTION) as board_db:
        board_db.begin()
        try:
            acl_table = board_db['acl']
            board_tbl = board_db['boards']
            acl = acl_table.find_one(user_id=user_data['user_id'], board_id=board_id)
            if acl is not None:
                acl_table.delete(board_id=board_id)
                board_tbl.delete(board_id=board_id)
                response.content_type = 'application/json; charset=utf-8'
                return json.dumps({'message': board_id + ' deleted'})
            else:
                return HTTPResponse(status=404)

        except:
            board_db.rollback()
            return HTTPResponse(status=404)


# prevent running with nosetests
if __name__ == '__main__':
    run(APP,
        host=CONFIG['board']['host'],
        port=CONFIG['board']['port'],
        debug=True,
        server='cherrypy')
