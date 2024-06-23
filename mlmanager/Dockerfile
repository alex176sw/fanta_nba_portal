FROM python:3.9-slim

WORKDIR /usr/src/app
RUN pip install --upgrade pip

COPY pyproject.toml .
RUN pip install -e .

COPY . .
RUN pip install -e .

EXPOSE 5000

CMD ["python", "/usr/src/app/mlmanager/main.py", "-c", "/usr/src/app/mlmanager/config/production.yaml"]
