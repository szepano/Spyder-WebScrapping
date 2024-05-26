import scrapy
from scrapy.settings import BaseSettings


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    @classmethod
    def update_settings(cls, settings: BaseSettings) -> None:
        settings.set('FEED_URI', 'authors.json', priority='spider')
        settings.set('FEED_FORMAT', 'json')
        

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            about_link = quote.xpath(".//a[contains(text(), '(about)')]/@href").get()
            if about_link:
                yield response.follow(url=about_link, callback=self.parse_about)

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
       

    def parse_about(self, response):
            for info in response.xpath("/html//div[@class='author-details']"):
                yield {
                    'fullname': info.xpath("h3[@class='author-title']/text()").get(),
                    'born_date': info.xpath("p/span[@class='author-born-date']/text()").get(),
                    'born_location': info.xpath("p/span[@class='author-born-location']/text()").get(),
                    'description': ' '.join(info.xpath("div[@class='author-description']/text()").getall()).strip()
                }

