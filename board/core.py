# -*- coding: utf-8 -*-
from board import helpers
from bottle import Bottle, run, response

app = Bottle()


@app.get('/board')
def getrequest():
    return helpers.listallboards(response)


@app.put('/board/<name:re:[a-z]*>')
def postrequest(name):
    return helpers.addboard(response, name)


@app.delete('/board/<id:re:[0-9]*')
def deleterequest(id):
    return helpers.removeboard(response, int(id))


# prevent running with nosetests
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
