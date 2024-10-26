FROM python:3.9

WORKDIR /App

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /App/wait-for-it.sh

ENTRYPOINT [ "python", "scraping_pipeline.py" ]
