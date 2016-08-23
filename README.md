# jak-services [![Build Status](https://travis-ci.org/reneleban/jak-services.svg?branch=master)](https://travis-ci.org/reneleban/jak-services)
Just another Kanban Board - Services

## initialize

* recommended: use virtualenv
* make init

## test

* make test

## docker 

docker build -t jak-base -f base.docker .;
docker build -t jak-login -f login.docker .;
docker run --rm -it -p 9090:9090 jak-login
