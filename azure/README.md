Create a cluster:
```
az aks create --resource-group aksResourceGroup --name askClusterDemo --enable-managed-identity --node-count 1 --generate-ssh-keys
```

Deploy the application:
```
kubectl apply -f aks-store-quickstart.yaml
```

Check if pods are running:
```
kubectl get pods
```

Get the IP address of the front-end service:
```
kubectl get service app-frontend
```

Destroy all:
```
kubectl delete deploy,pods,services --all
```


```
az group delete --name aksResourceGroup --yes --no-wait
```