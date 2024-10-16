from scrapy import Field
from .custom_item import CustomItem


class IslamwebConsultationItem(CustomItem):
    id = Field()
    title = Field()
    repliers = Field()
    watches_no = Field()
    date = Field()
    main_category = Field()
    question = Field()
    answer = Field()
