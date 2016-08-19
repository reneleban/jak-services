# -*- coding: utf-8 -*-
import json, configparser, logging, uuid, os

from bottle import Bottle, run, response
from jose import jwt


# read config file
config = configparser.ConfigParser()
config.read('config.ini')

LOCATION_DATA = config['board']['storage_location'] + os.path.sep + config['board']['storage_data']
LOCATION_ACL = config['board']['storage_location'] + os.path.sep + config['board']['storage_acl']

#configure logging
logging.basicConfig(filename='board.log',level=logging.DEBUG)

storagelist = []
accesslist = []

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
    return json.dumps(storagelist)


def restore():
    global storagelist, accesslist

    if len(storagelist) is 0:
        try:
            with open(LOCATION_DATA, 'r') as f:
                storagelist = json.load(f)
        except FileNotFoundError:
            logging.info("File not found: " + LOCATION_DATA)

    if len(accesslist) is 0:
        try:
            with open(LOCATION_ACL, 'r') as f:
                accesslist = json.load(f)
        except FileNotFoundError:
            logging.info('File not found: '+ LOCATION_ACL)


def addboard(user_uuid, response, name):
    global accesslist, storagelist

    board_uuid = uuid.uuid4()

    new_board = {'id': str(board_uuid), 'name': name}
    new_access = {'board_id' : str(board_uuid), 'user_id' : str(user_uuid)}

    storagelist.append(new_board)
    accesslist.append(new_access)

    updateStorage()

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(new_board)


def removeboard(user_uuid, response, board_id):
    global accesslist, storagelist

    count = len(storagelist)

    list = [x for x in storagelist if x['id'] == str(board_id)]
    removed_boards = []

    for item in list:
        for acl in accesslist:
            if acl['board_id'] == str(item['id']) and acl['user_id'] == str(user_uuid):
                storagelist.remove(item)

    new_access_list = [acl for acl in accesslist if acl['board_id'] != str(board_id)]
    accesslist = new_access_list;

    updateStorage()

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storagelist)})

def updateStorage():
    with open(LOCATION_DATA, 'w') as f:
        json.dump(storagelist, f)

    with open(LOCATION_ACL, 'w') as f:
        json.dump(accesslist, f)

# prevent running with nosetests
if __name__ == '__main__':
    run(app, host=config['board']['host'], port=config['board']['port'], debug=True, server='cherrypy')
