# -*- coding: utf-8 -*-
from board import helpers
from bottle import Bottle, run, template, response


app = Bottle()

@app.route('/hello/<name:re:[a-z]+>')
def hello(name='Wurst'):
    return template('Hello {{name}}!', name=name)

@app.get('/')
def getrequest():
    return helpers.testfunction(response)


@app.post('/')
def postrequest():
    return "POST"

# run(app, host='localhost', port=8080, debug=True)