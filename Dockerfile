FROM python:3.12.0


RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

CMD gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000