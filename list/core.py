# -*- coding: utf-8 -*-
from bottle import Bottle, run, response
import json, uuid, configparser, os, dataset

config = configparser.ConfigParser()
config.read('config.ini')

LOCATION_DATA = "sqlite:///" + config['list']['storage_location'] + os.path.sep + config['list']['storage_data']


class List(object):
    def __init__(self, list_id, board_id, name):
        self.board_id = board_id
        self.list_id = list_id
        self.name = name

    def dump(self):
        return {
            'board_id': self.board_id,
            'list_id': self.list_id,
            'name': self.name
        }


app = Bottle()


@app.get('/lists/list/<board_id>')
def get_all_elements(board_id):
    return lists_for_board(response, board_id)


@app.delete('/lists/list/<list_id>')
def remove(list_id):
    return remove_list(response, list_id)


@app.put('/lists/board/<board_id>/<name>')
def add_list_to_board(board_id, name):
    return add_list(response, board_id, name)


@app.delete('/lists/board/<board_id>')
def remove_lists(board_id):
    return remove_lists_for_board(response, board_id)


def lists_for_board(response, board_id):
    json_content(response)
    json_lists = []

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        list_table = db['list']
        lists = list_table.find(board_id=board_id)

        for row in lists:
            new_list = List(row['list_id'], row['board_id'], row['name'])
            json_lists.append(new_list)

    return json.dumps([l.dump() for l in json_lists])


def add_list(response, board_id, name):
    json_content(response)
    list_id = uuid.uuid4()
    new_list = List(str(list_id), str(board_id), name)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['list'].insert(new_list.__dict__)
            db.commit()
        except:
            db.rollback()

    return json.dumps(new_list.dump())


def remove_list(response, list_id):
    json_content(response)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['list'].delete(list_id=list_id)
            db.commit()
        except:
            db.rollback()

    return json.dumps({'deleted': True})


def remove_lists_for_board(response, board_id):
    json_content(response)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['list'].delete(board_id=board_id)
            db.commit()
        except:
            db.rollback()

    return json.dumps({'deleted': True})


def json_content(response):
    response.content_type = 'application/json; charset=utf-8'


if __name__ == '__main__':
    run(app, host='localhost', port=8081, debug=True)
