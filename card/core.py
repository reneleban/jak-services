import configparser
import json
import os
import uuid
import dataset

from bottle import Bottle, run, response
from jose import jwt


config = configparser.ConfigParser()
config.read('card.ini')

LOCATION_DATA = config['card']['sqlite_connect']


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
    return cards_for_list(response, list_id)


@app.delete('/cards/<token>/<card_id>')
def remove(token, card_id):
    userdata = extract_userdata(token)
    return remove_card(response, userdata['uuid'], card_id)


@app.put('/cards/<token>/<list_id>/<name>/<description>')
def add(token, list_id, name, description):
    userdata = extract_userdata(token)
    return add_card(response, userdata['uuid'], list_id, name, description)


def extract_userdata(token):
    return jwt.decode(token, config['jwt']['secret'], algorithms=[config['jwt']['algorithm']])


def add_card(response, owner, list_id, name, description):
    json_content(response)
    card_id = uuid.uuid4()
    new_card = Card(str(list_id), str(card_id), name, description, owner)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        db['card'].insert(new_card.__dict__)
        db.commit()

    return json.dumps(new_card.dump())


def remove_card(response, owner, card_id):
    json_content(response)

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        try:
            db['card'].delete(card_id=card_id, owner=owner)
            db.commit()
        except:
            db.rollback()

    return json.dumps({'deleted': True})


def cards_for_list(response, list_id):
    json_content(response)
    json_cards = []

    with dataset.connect(LOCATION_DATA) as db:
        db.begin()
        card_table = db['card']
        cards = card_table.find(list_id=list_id)

        for row in cards:
            new_card = Card(row['list_id'], row['card_id'], row['name'], row['description'], row['owner'])
            json_cards.append(new_card)

    return json.dumps([l.dump() for l in json_cards])


def json_content(response):
    response.content_type = 'application/json; charset=utf-8'


if __name__ == '__main__':
    run(app, host=config['card']['host'], port=config['card']['port'], debug=True)