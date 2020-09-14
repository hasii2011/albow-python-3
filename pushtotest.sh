#!/bin/bash

source venv-albow-Python-3.8.5/bin/activate

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deactivate
