import configparser
import json
import logging
import uuid
import dataset

from bottle import Bottle, run, response, request, HTTPResponse
from jose import jwt

config = configparser.ConfigParser()
config.read('card.ini')

LOCATION_DATA = config['card']['sqlite_connect']

logging.basicConfig(filename=config['card']['logfile'], level=logging.DEBUG)


class Card(object):
    def __init__(self, list_id, card_id, name, description, owner):
        self.list_id = list_id
        self.card_id = card_id
        self.name = name
        self.description = description
        self.owner = owner

    def dump(self):
        return {
            'list_id': self.list_id,
            'card_id': self.card_id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner
        }


app = Bottle()


@app.get('/cards/<token>/<list_id>')
def get_all_cards_for_list(token, list_id):
    json_content()
    json_cards = []

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        card_table = db['card']
        cards = card_table.find(list_id=list_id)

        for row in cards:
            new_card = Card(row['list_id'], row['card_id'], row['name'], row['description'],
                            row['owner'])
            json_cards.append(new_card)

    return json.dumps([l.dump() for l in json_cards])


@app.get('/count/<token>/<list_id>')
def get_count_cards_for_list(token, list_id):
    json_content()

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        card_table = db['card']
        count = card_table.count(list_id=list_id)

    return json.dumps({'count': count})


@app.delete('/cards/<token>/<card_id>')
def remove(token, card_id):
    logging.debug("Deleting card with id %s", card_id)
    user_data = extract_user_data(token)
    owner = user_data["user_id"]

    json_content()

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['card'].delete(card_id=card_id, owner=owner)
            db.commit()
        except:
            db.rollback()
            return HTTPResponse(status=404)

    return HTTPResponse(status=200)


@app.delete('/cards/list/<token>/<list_id>')
def remove_cards_for_list(token, list_id):
    user_data = extract_user_data(token)
    owner = user_data["user_id"]
    json_content()
    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['card'].delete(list_id=list_id, owner=owner)
            db.commit()
        except:
            db.rollback()
            return HTTPResponse(status=404)

    return HTTPResponse(status=200)


@app.post('/cards/<token>/<list_id>')
def add(token, list_id):
    user_data = extract_user_data(token)
    owner = user_data["user_id"]

    forms = request.forms
    name = forms.name
    description = forms.description

    if description is None:
        description = ""

    logging.debug("Adding card list_id=%s name=%s desc=%s", list_id, name, description)
    json_content()
    card_id = uuid.uuid4()
    new_card = Card(str(list_id), str(card_id), name, description, owner)

    with dataset.connect(LOCATION_DATA) as db:
        try:
            db.begin()
            db['card'].insert(new_card.__dict__)
            db.commit()
            logging.debug("Card has been added")
        except:
            logging.debug("Card could not be added")
            return HTTPResponse(status=500)

    return json.dumps(new_card.dump())


def extract_user_data(token):
    return jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])


def json_content():
    response.content_type = 'application/json; charset=utf-8'


if __name__ == '__main__':
    run(app,
        host=config['card']['host'],
        port=config['card']['port'],
        debug=True,
        server='cherrypy')
