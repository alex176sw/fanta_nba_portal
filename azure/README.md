https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli

Create a Resource Group:
```
az group create --name aksClusterResourceGroup --location italynorth
```

Create a cluster:
```
az aks create --resource-group aksClusterResourceGroup --name askClusterDemo --enable-managed-identity --node-count 1 --generate-ssh-keys
```
```
az aks get-credentials --resource-group aksClusterResourceGroup --name askClusterDemo
```

Deploy the application:
```
kubectl apply -f aks-deployment.yaml
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
az group delete --name aksClusterResourceGroup --yes --no-wait
```