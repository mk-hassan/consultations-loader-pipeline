from datetime import datetime
from itemadapter import ItemAdapter

from items import IslamwebConsultationItem


def _clean_list(arr: list) -> list:
    return list(filter(lambda x: len(x) != 0, map(lambda x: x.strip(), arr)))


class IslamwebConsultationPipeline:
    def process_item(self, item: IslamwebConsultationItem, spider):
        adapter = ItemAdapter(item)

        adapter["id"] = int(adapter["id"])
        adapter["title"] = adapter["title"].strip()
        adapter["watches_no"] = int(adapter["watches_no"])
        adapter["date"] = datetime.strptime(adapter["date"], "%Y-%m-%d")
        adapter["answer"] = "\n".join(_clean_list(adapter["answer"]))
        adapter["question"] = "\n".join(_clean_list(adapter["question"]))
        adapter["repliers"] = " - ".join(_clean_list(adapter["repliers"]))

        return item
