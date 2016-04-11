init:
	pip install -r requirements.txt
	python setup.py install


test:
	nosetests tests
