FROM python:3.9.6-alpine3.14

WORKDIR /App

COPY requirements.txt .

RUN apk update && apk upgrade
RUN apk add --no-cache sqlite
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "prefect", "server", "start" ]

# docker run --name crawler -it -d dlt/islamic_pipeline:v0.1