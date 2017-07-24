# -*- coding: utf-8 -*-
"""
.. module:: board
    :platform: osx, linux
    :synopsis: BOARD Rest Microservice for JAK
.. moduleauthor:: René Leban<leban.rene@gmail.com>
"""
import configparser
import json
import logging
import uuid
import dataset

from bottle import Bottle, run, response, HTTPResponse, request
from jose import jwt
from os import path

# read config file
CONFIG = configparser.ConfigParser()
CONFIG.read(path.normpath(path.join(path.abspath(path.dirname(__file__)), '../../', 'board.ini')))

# configure logging
logging.basicConfig(filename=CONFIG['board']['logfile'], level=logging.DEBUG)

SQLITE_CONNECTION = CONFIG['board']['sqlite_connect']

APP = Bottle()


@APP.get('/')
def getinfo():
    """
    GET: / --> Info message about implemented Operations
    :return: Simple HTML with some information's
    """
    return "<html><head><title>JAK-Board-Service</title></head><body>" \
           "<p>GET: <strong>/count/token</strong> - count available boards</p>" \
           "<p>GET: <strong>/board/token</strong> - list available boards</p>" \
           "<p>PUT: <strong>/board/[a-z]/token</strong> - add board</p>" \
           "<p>DELETE: <strong>/board/[0-9]/token</strong> - delete by ID</p>" \
           "</body></html>"


@APP.get('/count/<token>')
def count_all_boards(token):
    """
    GET: /count/<token> --> Count available boards for given user
    :param token: user token
    :return: JSON Count result or HTTPStatus 404
    """

    user_data = jwt.decode(token, CONFIG['jwt']['secret'], algorithms=[CONFIG['jwt']['algorithm']])
    logging.debug("count available boards for given user: " + user_data["user_id"])
    with dataset.connect(SQLITE_CONNECTION) as db:
        try:
            db.begin()
            board_table = db['boards']
            count = board_table.count()
            response.content_type = 'application/json; charset=utf-8'
            return json.dumps({'count': count})

        except:
            return HTTPResponse(status=404)


@APP.get('/board/<token>')
def list_all_boards(token):
    """
    GET: /board/<token> --> Request all boards for user with given token
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


@APP.post('/board/<token>')
def add_board(token):
    """
    POST: /board/<token> --> Insert new Board with given form param 'name' for user 'token'
    :param token: user token
    :return: JSON with board_id and name or HTTPStatus 404
    """
    name = request.forms.name
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
    DELETE: /board/<token>/<board_id> --> Remove board 'board_id' with user 'token'
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
                board_db.commit()
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
