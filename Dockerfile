FROM python:3.12.0


RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .  /fastapi_app

RUN chmod +x /fastapi_app/docker/app.sh
