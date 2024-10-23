from datetime import datetime
from itemadapter import ItemAdapter

from items import IslamwebConsultationItem


def _clean_list(arr: list) -> list:
    return list(filter(len, map(lambda x: x.strip(), arr)))


class IslamwebConsultationPipeline:
    def process_item(self, item: IslamwebConsultationItem, spider):
        adapter = ItemAdapter(item)

        adapter["id"] = int(adapter["id"])
        adapter["title"] = adapter["title"].strip()
        adapter["watch_count"] = int(adapter["watch_count"])
        adapter["date"] = datetime.strptime(adapter["date"], "%Y-%m-%d")
        adapter["repliers"] = _clean_list(adapter["repliers"])
        adapter["question"] = "\n".join(_clean_list(adapter["question"]))
        adapter["answer"] = "\n".join(_clean_list(adapter["answer"]))

        return item
