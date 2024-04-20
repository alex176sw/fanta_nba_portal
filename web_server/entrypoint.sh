#!/bin/bash

NODEP=$1
if [[ -z "$1" ]]; then
    echo "Using standard port 3000" 1>&2
    NODEP=3000
fi

PORT=$NODEP node app/index.js 