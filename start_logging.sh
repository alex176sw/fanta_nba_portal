#!/bin/bash

mkdir -p logs

# log each 1 second

while true; do
    docker compose logs mlmanager-service > ./logs/mlmanager-service.log 2>&1
    docker compose logs trainer-service > ./logs/trainer-service.log 2>&1
    docker compose logs inference-service > ./logs/inference-service.log 2>&1
    docker compose logs flask-app-preprocessing > ./logs/flask-app-preprocessing.log 2>&1
    sleep 2
done &

