.PHONY: test

checks: black pylint mypy test slowtest
	make -C doc html linkcheck

test:
	pytest -m "not slow"

slowtest:
	pytest

install:
	pip install pip-tools
	pip-sync requirements/requirements.txt

coverage:
	pytest --cov=fmi --cov-report term --cov-report html test

mypy:
	mypy fmi

black:
	black --check --diff .

lint: black pylint

pylint:
	pylint fmi

lint-fix:
	black .

publish:
	rm -rf dist
	python setup.py sdist
	twine upload dist/*
