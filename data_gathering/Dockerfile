FROM python:3.9-slim

WORKDIR /usr/src/app

COPY pyproject.toml .

RUN pip install --upgrade pip
RUN pip install -e .

COPY . .

EXPOSE 8000

CMD ["python", "/usr/src/app/fanta_nba_data_gathering_service/main.py", "-c", "/usr/src/app/fanta_nba_data_gathering_service/config/production.yaml"]
