#!/bin/bash
kubectl apply -f pv-azuredisk.yaml
kubectl apply -f pvc-azuredisk.yaml
for file in $(ls *.yaml); do
    kubectl apply -f $file
done