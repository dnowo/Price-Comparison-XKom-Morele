import scrapy
from scrapy.crawler import CrawlerProcess


class ShopsSpider(scrapy.Spider):
    name = "shop"

    def start_requests(self):
        urls = [
            # "https://www.euro.com.pl/",
            "https://www.morele.net/",
            "https://www.x-kom.pl/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        print(response.css('title'))
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(ShopsSpider)
process.start()
