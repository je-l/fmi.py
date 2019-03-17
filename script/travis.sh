#!/usr/bin/env bash

set -xeo pipefail

make install
make black
make mypy pylint slowtest

# documentation
make -C doc html linkcheck
