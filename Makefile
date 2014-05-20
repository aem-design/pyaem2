build: clean lint test coverage

clean:
	rm -rf *egg*
	rm -rf .coverage
	rm -rf htmlcov
	rm -f pyaem/*.pyc
	rm -f test/*.pyc
	rm -rf docs/*

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
	sphinx-apidoc -o docs --full -H PyAEM -A "Cliffano Subagio" pyaem
	mkdir -p docs/_themes && cd docs/_themes/ && git clone https://github.com/armstrong/armstrong_sphinx armstrong
	echo "html_theme = 'armstrong'\nhtml_theme_path = ['_themes', ]" >> docs/conf.py
	cd docs && PYTHONPATH=../../pyaem/ make html
	cd docs/_build/html && tar -cvf /tmp/pyaem-doc.tar .

publish-test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

publish:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

.PHONY: build clean lint test coverage coverage-publish doc
