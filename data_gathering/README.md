Execute outside the container:
```
python3 -m venv dgenv
source dgenv/bin/activate
pip install -e .
python ./fanta_nba_data_gathering_service/main.py -c ./fanta_nba_data_gathering_service/config/default.yaml
```


Build the container:
```
docker build -t alex176/azure-data-gathering-service:v1.1 .
docker push alex176/azure-data-gathering-service:v1.1
```


Execute the container:
```
docker container run --name data-gathering-app -d --network host alex176/azure-data-gathering-service:v1.1
```


Issue on connecting to stats.nba.com from a cloud provider: https://github.com/swar/nba_api/issues/176

 