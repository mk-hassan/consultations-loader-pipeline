from scrapy import Item


class CustomItem(Item):
    def toJson(self) -> dict:
        return {key: value for key, value in self.items()}
