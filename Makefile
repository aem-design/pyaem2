build: clean lint test coverage

clean:
	rm -rf .coverage
	rm -rf htmlcov
	rm -f pyaem/*.pyc
	rm -f test/*.pyc

deps-dev:
	pip install -r requirements-dev.txt

lint:
	pylint --rcfile=.pylintrc pyaem test

test:
	python setup.py test

coverage:
	coverage run setup.py test
	coverage report -m
	coverage html

.PHONY: clean lint test coverage all
