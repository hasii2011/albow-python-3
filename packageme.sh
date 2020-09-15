#!/bin/bash
#
#  Assumes python 3 is on PATH
#

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear

source venv-albow-Python-3.8.5/bin/activate
./cleanup.sh
python3 setup.py sdist bdist_wheel

# Check package
twine check dist/*
