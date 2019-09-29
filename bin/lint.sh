#!/bin/sh

python3 -m flake8 src/py && mypy src/py
