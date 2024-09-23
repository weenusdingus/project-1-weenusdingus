#!/bin/sh

if [ $# -ne 1 ]; then
    echo "usage: sh config_test.sh #"
    exit 1
fi

printf "[pytest]\npython_files = *$1*" > pytest.ini
pip install ".[classroom]"
