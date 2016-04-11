# -*- coding: utf-8 -*-
import json

from bottle import Bottle, run, response

# Location of the Data-File !
BOARD_DATA_JSON = '/tmp/board-data.json'

storagelist = []

app = Bottle()


@app.get('/')
def getinfo():
    return "<html><head></head><body>" \
           "<p>GET: <strong>/board</strong> - list all boards</p>" \
           "<p>PUT: <strong>/board/[a-z]</strong> - add board</p>" \
           "<p>DELETE: <strong>/board/[0-9]</strong> - delete by ID</p>" \
           "<p>DELETE: <strong>/board/[a-zA-Z\s]</strong> - delete by name</p>" \
           "</body></html>"


@app.get('/board')
@app.get('/board/')
def getrequest():
    restore()
    return listallboards(response)


@app.put('/board/<name:re:[a-zA-Z\s]*>')
def postrequest(name):
    restore()
    return addboard(response, name)


@app.delete('/board/<id:int>')
def deletebyidrequest(id):
    restore()
    return removeboard(response, int(id))


def listallboards(response):
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(storagelist)


def restore():
    global storagelist
    if len(storagelist) is 0:
        try:
            with open(BOARD_DATA_JSON, 'r') as f:
                storagelist = json.load(f)
        except FileNotFoundError:
            print("WARNING: data-file not found (" + BOARD_DATA_JSON + ")")


def addboard(response, name):
    id = len(storagelist) + 1
    new_board = {'id': id, 'name': name}
    storagelist.append(new_board)

    with open(BOARD_DATA_JSON, 'w') as f:
        json.dump(storagelist, f)

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(new_board)


def removeboard(response, id):
    count = len(storagelist)
    list = [x for x in storagelist if x['id'] == int(id)]
    for item in list:
        storagelist.remove(item)

    with open(BOARD_DATA_JSON, 'w') as f:
        json.dump(storagelist, f)

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storagelist)})


# prevent running with nosetests
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
