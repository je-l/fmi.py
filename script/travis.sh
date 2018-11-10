#!/usr/bin/env bash

set -xeo pipefail

pytest -v
make -C doc html linkcheck

if [[ "$TRAVIS_PYTHON_VERSION" = "3.5" ]]; then
  echo "skipping lint for python 3.5"
else
  make lint
fi
