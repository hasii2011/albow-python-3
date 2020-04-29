#!/bin/bash

source venv-albow-Python-3.7.3/bin/activate

twine upload  dist/*

deactivate
