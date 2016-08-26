# -*- coding: utf-8 -*-
from bottle import Bottle, run, response
from jose import jwt
import json, uuid, configparser, os, dataset

config = configparser.ConfigParser()
config.read('list.ini')

LOCATION_DATA = config['list']['sqlite_connect']


class List(object):
    def __init__(self, list_id, board_id, name, owner):
        self.board_id = board_id
        self.list_id = list_id
        self.name = name
        self.owner = owner

    def dump(self):
        return {
            'board_id': self.board_id,
            'list_id': self.list_id,
            'name': self.name,
            'owner': self.owner
        }


app = Bottle()


@app.get('/lists/list/<token>/<board_id>')
def get_all_elements(token, board_id):
    return lists_for_board(response, board_id)


@app.delete('/lists/list/<token>/<list_id>')
def remove(token, list_id):
    userdata = extract_userdata(token)
    return remove_list(response, userdata["user_id"], list_id)


@app.put('/lists/board/<token>/<board_id>/<name>')
def add_list_to_board(token, board_id, name):
    userdata = extract_userdata(token)
    return add_list(response, userdata["user_id"], board_id, name)


@app.delete('/lists/board/<token>/<board_id>')
def remove_lists(token, board_id):
    userdata = extract_userdata(token)
    return remove_lists_for_board(response, userdata["user_id"], board_id)


def extract_userdata(token):
    return jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])


def lists_for_board(response, board_id):
    json_content(response)
    json_lists = []

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        list_table = db['list']
        lists = list_table.find(board_id=board_id)

        for row in lists:
            new_list = List(row['list_id'], row['board_id'], row['name'], row['owner'])
            json_lists.append(new_list)

    return json.dumps([l.dump() for l in json_lists])


def add_list(response, owner, board_id, name):
    json_content(response)
    list_id = uuid.uuid4()
    new_list = List(str(list_id), str(board_id), name, str(owner))

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['list'].insert(new_list.__dict__)
            db.commit()
        except:
            db.rollback()

    return json.dumps(new_list.dump())


def remove_list(response, owner, list_id):
    json_content(response)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['list'].delete(list_id=list_id, owner=owner)
            db.commit()
        except:
            db.rollback()

    return json.dumps({'deleted': True})


def remove_lists_for_board(response, owner, board_id):
    json_content(response)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['list'].delete(board_id=board_id, owner=owner)
            db.commit()
        except:
            db.rollback()

    return json.dumps({'deleted': True})


def json_content(response):
    response.content_type = 'application/json; charset=utf-8'


if __name__ == '__main__':
    run(app, host=config['list']['host'], port=config['list']['port'], debug=True)
