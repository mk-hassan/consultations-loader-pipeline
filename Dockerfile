FROM python:3.9.6

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

# docker run --name crawler -it -d dlt/islamic_pipeline:v0.1