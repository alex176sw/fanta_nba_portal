FROM python:3.9-slim

WORKDIR /usr/src/app
RUN pip install --upgrade pip

COPY pyproject.toml .
RUN pip install -e .

COPY . .
RUN pip install -e .

EXPOSE 8000

CMD ["python", "/usr/src/app/trainer/main.py", "-c", "/usr/src/app/trainer/config/production.yaml"]
