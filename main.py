import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)

# class First_scrapyItem(scrapy.Item):
#     name = scrapy.Field()
#     url = scrapy.Field()
#     desc = scrapy.Field()
#
#
# class firstSpider(scrapy.Spider):
#     name = "first"
#     allowed_domains = ["x-kom.pl", "morele.net"]
#
#     start_urls = [
#         "https://www.x-kom.pl/",
#         "https://www.morele.net/"
#     ]
#
#     def parse(self, response):
#         filename = response.url.split("/")[-2] + '.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)
