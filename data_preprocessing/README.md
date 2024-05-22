Execute outside the container:
```
python3 -m venv dpenv
source dpenv/bin/activate
pip install -e .
python ./fanta_nba_data_preprocessing_service/main.py -c ./fanta_nba_data_preprocessing_service/config/default.yaml
```




Build del container:
```
docker build -t alex176/azure-data-preprocessing-service:v1.4 .
docker push alex176/azure-data-preprocessing-service:v1.4
```



Execute the container:
```
docker container run --name flask-app-preprocessing -d -p 5000:5000 --network host alex176/azure-data-preprocessing-service:v1.2
```
