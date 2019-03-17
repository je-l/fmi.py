#!/usr/bin/env bash

set -xeo pipefail

pip install pip-tools

if [[ "$TRAVIS_PYTHON_VERSION" = "3.5" ]]; then
  pip-sync requirements/requirements-py35.txt
  echo "skipping black for python 3.5"
else
  pip-sync requirements/requirements.txt
  make black
fi

make mypy pylint slowtest

# documentation
make -C doc html linkcheck
