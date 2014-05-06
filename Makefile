build: clean lint test coverage

clean:
	rm -rf .coverage
	rm -rf htmlcov
	rm -f pyaem/*.pyc
	rm -f test/*.pyc

deps:
	pip install -r requirements.txt

deps-dev:
	pip install -r requirements-dev.txt

lint:
	pylint --rcfile=.pylintrc pyaem test

test:
	python setup.py test

coverage:
	coverage run setup.py test
	coverage report --show-missing --fail-under=100
	coverage html

coverage-publish: coverage
	coveralls

.PHONY: build clean lint test coverage coverage-publish
