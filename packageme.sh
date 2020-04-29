#!/bin/bash
#
#  Assumes python 3 is on PATH
#
clear

source venv-albow-Python-3.7.3/bin/activate
./cleanup.sh
python3 setup.py sdist bdist_wheel

# Check package
twine check dist/*
