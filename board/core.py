# -*- coding: utf-8 -*-
from board import helpers
from bottle import Bottle, run, response

app = Bottle()


@app.get('/board')
def getrequest():
    return helpers.listallboards(response)


@app.post('/board/<name:re:[a-z]*>')
def postrequest(name):
    return helpers.addboard(response, name)


# prevent running with nosetests
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
