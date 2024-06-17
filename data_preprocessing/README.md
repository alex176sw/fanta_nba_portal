# FantaNBA Data-Preprocessing service
This is the middle-man between the MLManager service and the database. It transform the data read from the database to a suitable format for machine learning algorithms.

## Instructions
To build and push the Docker container:
```
docker build -t alex176/azure-data-preprocessing-service:v1.5 .
docker push alex176/azure-data-preprocessing-service:v1.5
```

To run the container:
```
docker container run --name flask-app-preprocessing -d -p 5000:5000 --network host alex176/azure-data-preprocessing-service:v1.5
```

Execute outside the container:
```
python3 -m venv dpenv
source dpenv/bin/activate
pip install -e .
python ./fanta_nba_data_preprocessing_service/main.py -c ./fanta_nba_data_preprocessing_service/config/default.yaml
```
