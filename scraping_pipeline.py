import dlt
from scraping import run_pipeline
from spiders import IslamwebspiderSpider

from dotenv import load_dotenv

load_dotenv(".env")

from prefect import flow, task
from prefect_email import EmailServerCredentials, email_send_message

import blocks.email_block
from data.messages import success_message, failure_message

import os
from datetime import datetime


@task(
    name="scraping-loading-consultations",
    log_prints=True,
    retries=3,
    retry_delay_seconds=100,
)
def scrape_consultations() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="consultations",
        destination="qdrant",
        dataset_name="consultations",
    )

    run_pipeline(
        pipeline,
        IslamwebspiderSpider,
        # you can pass scrapy settings overrides here
        scrapy_settings={
            "DEPTH_LIMIT": 10,
            "ITEM_PIPELINES": {
                "pipelines.IslamwebConsultationPipeline": 300,
            },
            "FEEDS": {
                "./output/scrapped-consultations.jsonl": {
                    "format": "jsonl",
                    "encoding": "utf8",
                    "overwrite": True,
                }
            },
        },
    )

    with open(f"./output/schema-{datetime.now()}.yml", "w") as schema:
        schema.write(pipeline.default_schema.to_pretty_yaml())


def email_send_message_flow(msg):
    email_server_credentials = EmailServerCredentials.load("email-notify")
    notified_email = os.getenv("NOTIFIED_EMAIL_ADDRESS")

    if notified_email == None:
        raise ValueError("email address should be provided")

    email_send_message.with_options(name=f"emailing {notified_email}").submit(
        email_server_credentials=email_server_credentials,
        subject=f"Monthly DLT Pipeline Flow Status Notification {datetime.now().date()}",
        msg="",
        msg_plain=msg,
        email_to=notified_email,
    ).wait()


@flow(name="main")
def main():
    admin_name = os.getenv("ADMIN_NAME")
    try:
        scrape_consultations()
        email_send_message_flow(
            success_message.format(user_name=admin_name, date=datetime.now())
        )
    except Exception as exc:
        email_send_message_flow(
            failure_message.format(
                user_name=admin_name,
                date=datetime.now(),
                error=exc,
            )
        )


# run it once, then schedule
if __name__ == "__main__":
    main()
    main.serve(
        name="scrapping_consultations_schedule",
        tags=["dlt-pipeline", "consultations"],
        description="running scrapy to qdarnt pipeline consulation loading",
        cron="0 0 1 * *",
    )
