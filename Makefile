build: clean lint test coverage

clean:
	rm -rf *egg*
	rm -rf .coverage
	rm -rf htmlcov
	rm -f pyaem2/*.pyc
	rm -f test/*.pyc
	rm -rf docs
	rm -rf build
	rm -rf dist

deps:
	export PYCURL_SSL_LIBRARY=openssl
	pip install -r requirements.txt

deps-dev:
	export PYCURL_SSL_LIBRARY=openssl
	pip install -r requirements-dev.txt

lint:
	pylint --rcfile=.pylintrc pyaem2 test

test:
	python setup.py test

coverage:
	coverage run setup.py test
	coverage html
	coverage report --show-missing --fail-under=100
	py.test  --cov-report term --cov=test/

coverage-publish:
	coverage
	coveralls

codecov:
	coverage
	codecov

codecov-publish:
	codecov
	codecov

doc:
	sphinx-apidoc -o docs --full -H PyAEM2 -A "Max Barrass" pyaem2
	cd docs && \
		SPHINXOPTS="-D html_theme=sphinx_rtd_theme \
			-D extensions=sphinx.ext.autodoc,sphinx.ext.viewcode,sphinx.ext.todo,sphinx_rtd_theme" \
		PYTHONPATH=../../pyaem2/ \
		make html
	touch docs/_build/html/.nojekyll
	cd docs/_build/html && tar -cvf /tmp/pyaem2-doc.tar .

publish-test:
	python setup.py sdist bdist_wheel
	twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/ dist/*

publish:
	python setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*

.PHONY: build clean lint test coverage
