.PHONY: test

init:
	pip install '.[docs,dev]'

test:
	pytest

coverage:
	pytest --cov=fmi --cov-report term --cov-report html test

lint:
	pylint fmi

publish:
	rm -rf dist
	python setup.py sdist
	twine upload dist/*
