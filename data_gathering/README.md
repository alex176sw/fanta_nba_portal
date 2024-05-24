# FantaNBA Data-Gathering service
This micro-service responsability is to download, every day, the nba data from the nba_api data provider. Then it transform the raw data into statistics and save them into the mongo db main database.

There's an issue on connecting to stats.nba.com from a cloud provider: https://github.com/swar/nba_api/issues/176


## Instructions

To build and push the Docker container:
```
docker build -t alex176/azure-data-gathering-service:v1.2 .
docker push alex176/azure-data-gathering-service:v1.2
```

Execute the container:
```
docker container run --name data-gathering-app -d --network host alex176/azure-data-gathering-service:v1.2
```

 Execute outside the container:
```
python3 -m venv dgenv
source dgenv/bin/activate
pip install -e .
python ./fanta_nba_data_gathering_service/main.py -c ./fanta_nba_data_gathering_service/config/default.yaml
```
