# FantaNBA Inference service
This service is responsible for making predictions using the models stored in the MLDatabase.

## Instructions

To build and push the Docker container:
```
docker build -t alex176/inference-service:v1.0 .
docker push alex176/inference-service:v1.0
```

To run the container:
```
docker container run --name inference -d --network host alex176/inference-service:v1.0
```

Execute outside the container:
```
python3 -m venv fantanba-env
source fantanba-env/bin/activate
pip install -e .
python ./inference/main.py -c ./inference/config/default.yaml
```
