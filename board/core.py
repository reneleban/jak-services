# -*- coding: utf-8 -*-
import configparser
import json
import logging
import os
import uuid

from bottle import Bottle, run, response
from jose import jwt


# read config file
config = configparser.ConfigParser()
config.read('config.ini')

LOCATION_DATA = config['board']['storage_location'] + os.path.sep + config['board']['storage_data']
LOCATION_ACL = config['board']['storage_location'] + os.path.sep + config['board']['storage_acl']

# configure logging
logging.basicConfig(filename=config['board']['logfile'], level=logging.DEBUG)

storage_list = []
access_list = []

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
    logging.debug('token: '+token)
    userdata = jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])
    logging.debug('user: '+userdata["uuid"])
    restore()
    return listallboards(response)


@app.put('/board/<token>/<name:re:[a-zA-Z\s]*>')
def postrequest(name, token):
    logging.debug('token: '+token)
    userdata = jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])
    restore()
    return addboard(userdata['uuid'], response, name)


@app.delete('/board/<token>/<board_id>')
def deletebyidrequest(board_id, token):
    logging.debug('token: '+token)
    userdata = jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])
    restore()
    return removeboard(userdata['uuid'], response, board_id)


def listallboards(response):
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(storage_list)


def restore():
    global storage_list, access_list

    if len(storage_list) is 0:
        try:
            with open(LOCATION_DATA, 'r') as f:
                storage_list = json.load(f)
        except FileNotFoundError:
            logging.info("File not found: " + LOCATION_DATA)

    if len(access_list) is 0:
        try:
            with open(LOCATION_ACL, 'r') as f:
                access_list = json.load(f)
        except FileNotFoundError:
            logging.info('File not found: '+ LOCATION_ACL)


def addboard(user_uuid, response, name):
    global access_list, storage_list

    board_uuid = uuid.uuid4()

    new_board = {'id': str(board_uuid), 'name': name}
    new_access = {'board_id' : str(board_uuid), 'user_id' : str(user_uuid)}

    storage_list.append(new_board)
    access_list.append(new_access)

    updateStorage()

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(new_board)


def removeboard(user_uuid, response, board_id):
    global access_list, storage_list

    count = len(storage_list)

    list = [x for x in storage_list if x['id'] == str(board_id)]
    removed_boards = []

    for item in list:
        for acl in access_list:
            if acl['board_id'] == str(item['id']) and acl['user_id'] == str(user_uuid):
                storage_list.remove(item)

    new_access_list = [acl for acl in access_list if acl['board_id'] != str(board_id)]
    access_list = new_access_list

    updateStorage()

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storage_list)})


def updateStorage():
    with open(LOCATION_DATA, 'w') as f:
        json.dump(storage_list, f)

    with open(LOCATION_ACL, 'w') as f:
        json.dump(access_list, f)

# prevent running with nosetests
if __name__ == '__main__':
    run(app, host=config['board']['host'], port=config['board']['port'], debug=True, server='cherrypy')
