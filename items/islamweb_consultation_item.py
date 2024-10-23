from scrapy import Field
from .custom_item import CustomItem


class IslamwebConsultationItem(CustomItem):
    id = Field()
    title = Field()
    repliers = Field()
    watch_count = Field()
    date = Field()
    category = Field()
    question = Field()
    answer = Field()
