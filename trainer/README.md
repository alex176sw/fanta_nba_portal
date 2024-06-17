# FantaNBA Trainer service
This service is responsible for training the models and storing them in the MLDatabase.


## Instructions

To build and push the Docker container:
```
docker build -t alex176/trainer-service:v1.0 .
docker push alex176/trainer-service:v1.0
```

To run the container:
```
docker container run --name ml-manager -d --network host alex176/trainer-service:v1.0
```

Execute outside the container:
```
python3 -m venv fantanba-env
source fantanba-env/bin/activate
pip install -e .
python ./trainer/main.py -c ./trainer/config/default.yaml
```
