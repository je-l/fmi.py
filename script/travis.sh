#!/usr/bin/env bash

set -eo pipefail

pytest -v

if [[ "$TRAVIS_PYTHON_VERSION" = "3.5" ]]; then
  echo "skipping lint for python 3.5"
else
  make lint
fi
