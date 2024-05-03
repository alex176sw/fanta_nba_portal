FROM python:3.9-slim

WORKDIR /usr/src/app

COPY pyproject.toml .

RUN pip install --upgrade pip
RUN pip install -e .

COPY . .

EXPOSE 8000

CMD ["python", "/usr/src/app/dg/main.py", "-c", "/usr/src/app/dg/config/production.yaml"]
