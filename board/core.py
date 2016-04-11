# -*- coding: utf-8 -*-
import json

from bottle import Bottle, run, response

app = Bottle()
storagelist = []


class Board:
    id = 0
    name = ""

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def dump(self):
        return {"Board": {
            'id': self.id,
            'name': self.name
        }}


@app.get('/')
def getinfo():
    return "<html><head></head><body>" \
           "<p>GET: <strong>/board</strong> - list all boards</p>" \
           "<p>PUT: <strong>/board/[a-z]</strong> - add board</p>" \
           "<p>DELETE: <strong>/board/[0-9]</strong> - delete by ID</p>"\
           "<p>DELETE: <strong>/board/[a-zA-Z\s]</strong> - delete by name</p>"\
           "</body></html>"

@app.get('/board')
def getrequest():
    return listallboards(response)


def listallboards(response):
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps([o.dump() for o in storagelist])


@app.put('/board/<name:re:[a-z]*>')
def postrequest(name):
    return addboard(response, name)


def addboard(response, name):
    id = len(storagelist) + 1
    new_board = Board(id, name)
    storagelist.append(new_board)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(new_board.dump())


@app.delete('/board/<id:re:[0-9]*')
def deletebyidrequest(id):
    return removeboard(response, int(id))


def removeboard(response, id):
    count = len(storagelist)
    list = [x for x in storagelist if x.id == int(id)]
    for item in list:
        storagelist.remove(item)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storagelist)})


@app.delete('/board/<id:re:[a-zA-Z\s]*')
def deletebynamerequest(name):
    return removeboardbyname(response, str(name))


def removeboardbyname(response, name):
    count = len(storagelist)
    list = [x for x in storagelist if x.name == name]
    for item in list:
        storagelist.remove(item)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storagelist)})


# prevent running with nosetests
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
