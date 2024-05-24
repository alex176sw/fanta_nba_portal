FROM python:3.9-slim

WORKDIR /usr/src/app

COPY pyproject.toml .
COPY . .

RUN pip install --upgrade pip
RUN pip install -e .

EXPOSE 5000

CMD ["python", "/usr/src/app/fanta_nba_data_preprocessing_service/main.py", "-c", "/usr/src/app/fanta_nba_data_preprocessing_service/config/production.yaml"]
