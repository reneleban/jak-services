import json


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


storagelist = []


def listallboards(response):
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps([o.dump() for o in storagelist])


def addboard(response, name):
    id = len(storagelist) + 1
    new_board = Board(id, name)
    storagelist.append(new_board)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(new_board.dump())


def removeboard(response, id):
    count = len(storagelist)
    list = [x for x in storagelist if x.id == int(id)]
    for item in list:
        storagelist.remove(item)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storagelist)})

def removeboardbyname(response, name):
    count = len(storagelist)
    list = [x for x in storagelist if x.name == name]
    for item in list:
        storagelist.remove(item)
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({'message': count > len(storagelist)})
