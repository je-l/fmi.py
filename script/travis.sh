#!/usr/bin/env bash

set -xeo pipefail

pip install pip-tools

if [[ "$TRAVIS_PYTHON_VERSION" = "3.5" ]]; then
  pip-sync requirements/requirements-py35.txt
  echo "skipping lint for python 3.5"
else
  pip-sync requirements/requirements.txt
  make lint
fi

pytest -v
make -C doc html linkcheck
