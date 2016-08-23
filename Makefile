init:
	pip install -r requirements.txt
	python setup.py install

docker-base:
	docker build -t jak-base -f base.docker .;

docker-apps:
	docker build -t jak-login -f login.docker .;
	docker build -t jak-board -f board.docker .;
	docker build -t jak-list -f list.docker .;
	docker build -t jak-card -f card.docker .;

test:
	nosetests tests
