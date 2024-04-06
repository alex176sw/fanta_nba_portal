#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Must provide PORT in environment" 1>&2
    exit 1
fi

PORT=$1 node app/index.js 