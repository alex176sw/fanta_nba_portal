FROM python:3.9-slim

WORKDIR /usr/src/app

COPY pyproject.toml .
COPY . .

RUN pip install --upgrade pip
RUN pip install -e .


EXPOSE 8000

CMD ["python", "/usr/src/app/dbsynch/main.py", "-c", "/usr/src/app/dbsynch/config/production.yaml"]
