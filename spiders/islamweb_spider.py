from scrapy import Spider
from items import IslamwebConsultationItem


class IslamwebspiderSpider(Spider):
    allowed_domains = ["www.islamweb.net"]

    def parse(self, response):
        consults_categories = response.css(".right-nav.fatwalist .mainitem .tab_2 ul a")
        yield from response.follow_all(consults_categories, callback=self.parse)

        if not len(consults_categories):
            consults_links = response.css(
                ".right-nav.fatwalist .mainitem ~ ul.oneitems li h2 a"
            )
            yield from response.follow_all(consults_links, callback=self.parse_consult)

            next_page_link = response.css(
                ".Page-navigation li.active + li a::attr('href')"
            ).get()
            if next_page_link:
                yield response.follow(next_page_link, callback=self.parse)

    def parse_consult(self, response):
        consult_header = response.xpath("//*[@class='item-fatwa']")[0]
        consult_meta_dat = consult_header.xpath(".//samp")
        question, answer, *_ = consult_header.xpath("./following-sibling::div")

        islamwebConsultation = IslamwebConsultationItem()

        islamwebConsultation["id"] = consult_meta_dat[1].xpath("./a/text()").get()
        islamwebConsultation["title"] = consult_header.xpath(".//h2//text()").get()
        islamwebConsultation["repliers"] = (
            consult_meta_dat[0].xpath("./a/text()").getall()
        )
        islamwebConsultation["watch_count"] = (
            consult_meta_dat[2].xpath("./a/text()").get()
        )
        islamwebConsultation["date"] = consult_meta_dat[3].xpath("./a/text()").get()
        islamwebConsultation["question"] = question.xpath(".//p//text()").getall()
        islamwebConsultation["answer"] = answer.xpath(".//p//text()").getall()
        islamwebConsultation["category"] = response.xpath(
            "//*[@class='title-page']//ol/li[2]//span/text()"
        ).get()

        yield islamwebConsultation
