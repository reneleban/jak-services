# jak-services [![Build Status](https://travis-ci.org/reneleban/jak-services.svg?branch=master)](https://travis-ci.org/reneleban/jak-services) [![codecov](https://codecov.io/gh/reneleban/jak-services/branch/master/graph/badge.svg)](https://codecov.io/gh/reneleban/jak-services)
Just another Kanban Board - Services

## login-service

User management, authentication

### GET /login

uses basic authentication to check user credentials
* returns 200 and JSON String with token on success
* returns 404 on error

### POST /login

create new user using form parameters 'username' and 'password'
* returns 200 and JSON String with token on success
* returns 409 on conflict if user already exists
* returns 404 on other errors

### DELETE /login

delete user using basic auth, not via token to force re-authentication
of users
* returns 200 if ok
* returns 404 on error

## board-service

manage boards using token

### GET /board/{token}

* retrieves list of all boards for user with given token
 
### PUT /board/{token}/{name}

* add new board for user with given token

### DELETE /board/{token}/{board_id}

* check acl for user with token 
    * if granted delete board with given board_id
    * if denied throw Response Code 404

## initialize

* recommended: use virtualenv
* make init

## test

* make test

