#!/bin/bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

python3 -m test.RunTests

status=$?

echo "Exit with status: ${status}"
exit ${status}

