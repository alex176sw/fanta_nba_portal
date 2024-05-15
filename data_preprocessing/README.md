Execute outside the container:
```
python3 -m venv dpenv
source dpenv/bin/activate
pip install -e .
python ./fanta_nba_data_preprocessing_service/main.py -c ./fanta_nba_data_preprocessing_service/config/default.yaml
```




Build del container:
```
docker build -t alex176/azure-data-preprocessing-servivce:v1 .
```



Execute the container:
```
docker container run --name data-preprocessing-app -d -p 8000:8000 --network host alex176/azure-data-preprocessing-servivce:v1
```
