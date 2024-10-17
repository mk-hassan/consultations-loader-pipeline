import dlt
from scraping import run_pipeline
from spiders import IslamwebspiderSpider


def scrape_quotes() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="islamic_consultations",
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
        },
        primary_key="id",
        table_name="islamweb",
        write_disposition="merge",
    )

    with open("schema.yml", "w") as schema:
        schema.write(pipeline.default_schema.to_pretty_yaml())


if __name__ == "__main__":
    scrape_quotes()
