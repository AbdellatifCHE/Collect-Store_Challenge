import scrapy
import sys

class MySpider(scrapy.Spider):
    name = 'testing'
    #allowed_domains = ['theguardian.com']
    start_urls = [
                    'https://www.theguardian.com/science?page=1'
                ]

    def parse(self, response):
        if  response.css('h1::text').get() != ' ':
            yield {
                'URL' : "https://www.theguardian.com"+response.css('html::attr(data-page-path)').get(),
                'Title' : (response.css('h1::text').get()),
                'Date' : response.css('time::text').get(),
                'Author(s)' : response.css('a.tone-colour span::text').getall(),
                'Content' : response.css('div.content__article-body p::text').getall()
                }
        #response.xpath('//a[@class="u-faux-block-link__overlay js-headline-text"]/@href').extract() or response.css('a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall()
        for article_url in response.css('section.fc-container.fc-container--tag a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall():
            yield scrapy.Request(response.urljoin(article_url), self.parse)
        
        
        next_page = response.css('a.button.button--small.button--tertiary.pagination__action--static[rel="next"]::attr(href)').get()
        if next_page == "https://www.theguardian.com/science?page=101":
            sys.exit("Limit reached !")
        yield scrapy.Request(response.urljoin(next_page), self.parse)
             
#testing1.json: For performance reasons, document symbols have been limited to 5000 items.
#Use setting 'json.maxItemsComputed' to configure the limit.

#Start at 18:07:01
#Finished at 18:32:28