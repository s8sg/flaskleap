.PHONY: help requirments clean clean-build clean-pyc lint test test-all docs release install install-dev install-docker

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "install-dev - install the package for the develope env"

requirments: 
	pip install -r requirements.txt

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 {{ service_name }} test

test: requirments
	python setup.py coverage

test-all:
	tox

docs:
	rm -f docs/{{ service_name }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ service_name }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: requirments clean
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel upload

sdist: requirments clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist

install: requirments clean
	python setup.py install

install-dev: requirments clean 
	python setup.py develop

install-docker:
	sh ./build-steps/build-docker.sh {{ service_name }}-local {{ AUTHOR }}/{{ service_name}}

release-docker:
	sh ./build-steps/release-docker.sh {{ AUTHOR }}/{{ service_name }} {{ service_name }}-service $(VERSION)
