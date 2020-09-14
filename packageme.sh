#!/bin/bash
#
#  Assumes python 3 is on PATH
#
clear

source venv-albow-Python-3.8.5/bin/activate
./cleanup.sh
python3 setup.py sdist bdist_wheel

# Check package
twine check dist/*
