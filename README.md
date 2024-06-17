# FantaNBA portal
The application is composed by the following micro-services:
* FantaNBA front-end service: [README](web_server/README.md)
* FantaNBA data-preprocessing service: [README](data_preprocessing/README.md)
* FantaNBA database and database-synch services: [README](database/README.md)
* FantaNBA data gathering service: [README](data_gathering/README.md)
* FantaNBA mlmanager service: [README](mlmanager/README.md)
* FantaNBA mldatabase service: [README](database/README.md)
* FantaNBA trainer service: [README](trainer/README.md)
* FantaNBA inference service: [README](inference/README.md)

The azure deployment is described [here](azure/README.md)


## How to start the application

### Local deployment
To start the application locally:
```bash
docker compose up -d --build --force-recreate --remove-orphans 
```

### Azure deployment
To start the application in Azure:
```bash
docker compose build
docker login
docker compose push

az group create --name fanta-nba --location eastus
az deployment group create --resource-group fanta-nba --template-file azure/deployment.json --parameters azure/parameters.json
```

### Terraform deployment
To start the application in Azure using Terraform:
```bash
docker compose build
docker login
docker compose push

cd azure/terraform
terraform init
terraform apply
```

