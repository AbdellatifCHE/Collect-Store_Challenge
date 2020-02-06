import scrapy

class MySpider(scrapy.Spider):
    name = 'testing'
    #allowed_domains = ['example.com']
    start_urls = [
        'https://www.theguardian.com/science?page=2'
        #'https://www.theguardian.com/science?page=2/',
        #'https://www.theguardian.com/science?page=3/'
    ]

    def parse(self, response):
        #for h3 in response.xpath('//h1').getall():
        yield {
                'URL' : "https://www.theguardian.com"+response.css('html::attr(data-page-path)').get(),
              'Title' : response.css('h1::text').get(),
              'Date' : response.css('time::text').get(),
              'Author(s)' : response.css('a.tone-colour span::text').getall(),
              'Content' : response.css('div.content__article-body p::text').getall()
            }
        #response.xpath('//a[@class="u-faux-block-link__overlay js-headline-text"]/@href').extract() or response.css('a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall()
        for article_url in response.css('section.fc-container.fc-container--tag a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall():
            yield scrapy.Request(response.urljoin(article_url), self.parse)
             
#testing1.json: For performance reasons, document symbols have been limited to 5000 items.
#Use setting 'json.maxItemsComputed' to configure the limit.