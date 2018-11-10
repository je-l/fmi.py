.PHONY: test

test:
	pytest -m "not slow"

travis:
	./script/travis.sh

init:
	pip install '.[docs,dev]'

coverage:
	pytest --cov=fmi --cov-report term --cov-report html test

lint:
	black --check --diff .

lint-fix:
	black .

publish:
	rm -rf dist
	python setup.py sdist
	twine upload dist/*
