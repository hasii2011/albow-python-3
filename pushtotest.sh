#!/bin/bash

source venv-albow-Python-3.7.3/bin/activate

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deactivate
