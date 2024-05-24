import scrapy
from scrapy.settings import BaseSettings


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    @classmethod
    def update_settings(cls, settings: BaseSettings) -> None:
        settings.set('FEED_URI', 'authors.json', priority='spider')
        

    def parse(self, response):
       for quote in response.xpath("/html//div[@class='quote']"):
            about_link = quote.xpath(".//a[contains(text(), '(about)')]/@href").get()
            if about_link:
                print(about_link)
            else:
                print('value not found')
