#!/bin/bash

source venv-albow-Python-3.8.5/bin/activate

twine upload  dist/*

deactivate
