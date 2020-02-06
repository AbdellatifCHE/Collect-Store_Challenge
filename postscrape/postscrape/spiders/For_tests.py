import scrapy

class MySpider(scrapy.Spider):
    name = 'test'
    #allowed_domains = ['example.com']
    start_urls = [
        'https://www.theguardian.com/science/all/'
        #'https://www.theguardian.com/science?page=2/',
        #'https://www.theguardian.com/science?page=3/'
    ]

    def parse(self, response):
        for h3 in response.xpath('//h1').getall():
            yield {"title": h3}

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)