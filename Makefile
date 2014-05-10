build: clean lint test coverage doc

clean:
	rm -rf *egg*
	rm -rf .coverage
	rm -rf htmlcov
	rm -f pyaem/*.pyc
	rm -f test/*.pyc
	rm -rf docs/_build/*

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

doc:
	sphinx-apidoc -o docs --full pyaem
	cd docs && PYTHONPATH=../../pyaem/ make html && cd ..

.PHONY: build clean lint test coverage coverage-publish doc
