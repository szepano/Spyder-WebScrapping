import scrapy
from scrapy.settings import BaseSettings


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    @classmethod
    def update_settings(cls, settings: BaseSettings) -> None:
        settings.set('FEED_URI', 'quotes.json', priority='spider')

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        
        next_page = response.xpath("//li[@class='next']/a/href").get()
        if next_page:
            yield scrapy.Request(url=self.start_urls[0] + next_page, callback=self.parse)
