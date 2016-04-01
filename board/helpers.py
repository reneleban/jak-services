import json

test = [1, True, 3, {'4': 5, '6': 7}]


def testfunction(response):
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(test)