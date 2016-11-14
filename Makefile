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

docker-volumes:
	docker volume create --name jak-login-storage;
	docker volume create --name jak-board-storage;
	docker volume create --name jak-list-storage;
	docker volume create --name jak-card-storage;
	echo "run with: docker run -d -v jak-login-storage:/application/data -p 10030:10030 jak-login"
	
docker-remove-images:
	for line in $(docker images --format "{{.ID}};{{.Repository}}"|grep jak); do; image=${line%%;*}; docker rmi $image; done;

docker-update-card:
	docker stop jak-card
	docker rm jak-card
	docker rmi jak-card
	docker build -t jak-card -f card.docker .;
	docker run -d -v jak-card-storage:/application/data -p 10020:10020 --restart=always --name jak-card jak-card

docker-update-login:
	docker stop jak-login
	docker rm jak-login
	docker rmi jak-login
	docker build -t jak-login -f login.docker .;
	docker run -d -v jak-login-storage:/application/data -p 10030:10030 --restart=always --name jak-login jak-login

docker-update-list:
	docker stop jak-list
	docker rm jak-list
	docker rmi jak-list
	docker build -t jak-list -f list.docker .;
	docker run -d -v jak-list-storage:/application/data -p 10010:10010 --restart=always --name jak-list jak-list

docker-update-board:
	docker stop jak-board
	docker rm jak-board
	docker rmi jak-board
	docker build -t jak-board -f board.docker .;
	docker run -d -v jak-board-storage:/application/data -p 10000:10000 --restart=always--name jak-board jak-board

lint:
	pylint src/*

test:
	nosetests tests
