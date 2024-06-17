# FantaNBA MLManager service
This is the middle-man between the front-end and the MLDatabase. It exposes an API to the front-end to interact with the MLDatabase.


## Instructions

To build and push the Docker container:
```
docker build -t alex176/mlmanager-service:v1.0 .
docker push alex176/mlmanager-service:v1.0
```

To run the container:
```
docker container run --name ml-manager -d -p 5001:5001 --network host alex176/mlmanager-service:v1.0
```

Execute outside the container:
```
python3 -m venv fantanba-env
source fantanba-env/bin/activate
pip install -e .
python ./mlmanager/main.py -c ./mlmanager/config/default.yaml
```
