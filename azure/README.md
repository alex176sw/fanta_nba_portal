# FantaNBA Azure Deployment
Check the yaml files.

## Instructions

Resources: https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli


### Deploy
To start, we need a Resource Group. I'm going to use `srs2024-stu-g9` from Unibo. 

Create a cluster:
```
az aks create --resource-group srs2024-stu-g9 --name FantaNBACluster --enable-managed-identity --node-count 1 --generate-ssh-keys
```

Get credentials to connect to the azure app from the terminal:
```
az aks get-credentials --resource-group srs2024-stu-g9 --name FantaNBACluster
```

Enable the disk driver:
```
az aks update --name FantaNBACluster --resource-group srs2024-stu-g9 --enable-disk-driver
```

Create a disk:
```
az disk create --resource-group srs2024-stu-g9 --name mongodbDisk --size-gb 20 --query id --output tsv
```

Update the pv-azuredisk.yaml file with the disk id obtained from the previous command:
```
spec -> csi -> volumeHandle
```

Create secrets for the databases:
```
kubectl create secret generic db-pass --from-literal=db-password='m0ng0d8'
kubectl create secret generic db-user --from-literal=db-username='mongodb-user'
```


Deploy the application:
```
./apply_all.sh
```

### Checks
Check if pods are running:
```
kubectl get pods
```
Get the IP address of the services:
```
kubectl get services
```
Check if disks are created:
```
kubectl get pvc
```

### Unprovision
Destroy all:
```
kubectl delete deploy,pods,services --all
az group delete --name aksClusterResourceGroup --yes --no-wait
```

## Notes

### Scaling
Kubernetes uses the horizontal pod autoscaler (HPA) to monitor the resource demand and automatically scale the number of pods. As the HPA is effectively updated every 60 seconds, previous scale events may not have successfully completed before another check is made. This behavior could cause the HPA to change the number of replicas before the previous scale event could receive application workload and the resource demands to adjust accordingly. The default delay on scale down events is 5 minutes.

To respond to changing pod demands, the Kubernetes cluster autoscaler adjusts the number of nodes based on the requested compute resources in the node pool. By default, the cluster autoscaler checks the Metrics API server every 10 seconds for any required changes in node count. If the cluster autoscaler determines that a change is required, the number of nodes in your AKS cluster is increased or decreased accordingly. 

### Stess test
```
loadTestResource=cluster_stress_test
resourceGroup=srs2024-stu-g9
location=northeurope
az load create --name $loadTestResource --resource-group $resourceGroup --location $location
az load show --name $loadTestResource --resource-group $resourceGroup
```
To create a load test for a web endpoint:

- Go to the [Overview page of your Azure Load Testing resource](https://portal.azure.com/#@live.unibo.it/resource/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g9/overview).

- On the Get started tab, select Add HTTP requests > Create.


### Disks
Resources: https://learn.microsoft.com/en-us/azure/aks/azure-csi-disk-storage-provision#statically-provision-a-volume
```
Disk resource ID: /subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g9/providers/Microsoft.Compute/disks/myAKSDisk
```
 