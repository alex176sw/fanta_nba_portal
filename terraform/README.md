# Terraform - Infrastructure-as-code

Deploy applications into your AKS cluster using Terraform: https://developer.hashicorp.com/terraform/tutorials/azure-get-started/infrastructure-as-code

## Create a Terraform configuration to deploy an Azure resource group. 

1. Login to Azure
```
az login

az account set --subscription 0e9d7acf-5f4d-4c88-9ad9-45e8b7618ae9
```

2. Create a Service Principal: it is an application within Azure Active Directory with the authentication tokens Terraform needs to perform actions on your behalf. 
```
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/0e9d7acf-5f4d-4c88-9ad9-45e8b7618ae9"
```
=> Unibo subscription has insufficient privileges to complete the operation.

3. Write appId and appPassword into `terraform.tvars` and `variables.tf`.

4. Initialize your Terraform workspace, which will download the provider and initialize it with the values provided in your terraform.tfvars file.
```
terraform init
```

5. Provision the AKS cluster:
```
terraform apply
```

6. Connect to the cluster with kubectl and deploy the software

```
az aks get-credentials --resource-group $(terraform output -raw resource_group_name) --name $(terraform output -raw kubernetes_cluster_name)


kubectl apply -f <deployment-files.yaml>
```

7. Un-provision the AKS cluster:
```
terraform destroy
```
