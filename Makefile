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
	
docker-remove-images:
	for line in $(docker images --format "{{.ID}};{{.Repository}}"|grep jak); do; image=${line%%;*}; docker rmi $image; done;

test:
	nosetests tests
