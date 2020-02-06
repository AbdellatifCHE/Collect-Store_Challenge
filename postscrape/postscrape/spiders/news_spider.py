import scrapy

class PostsSpider(scrapy.Spider):
    name = 'news'
    #allowed_domains = ["bbc.com"]
    toto = [
                    'https://www.theguardian.com/science/all/'
                ]
    start_urls = toto
    #page_articles = response.css('a.u-faux-block-link__overlay::attr(href)').get()
    def parse(self, response):
        for article_url in response.css('a.u-faux-block-link__overlay::attr(href)').getall():#20 articles by page
            article_url = response.urljoin(article_url)
            yield scrapy.Request(article_url, self.parse)

            #for post in response.css('div.post-item'):
            yield 
            {
              'URL' : "https://www.theguardian.com"+response.css('html::attr(data-page-path)').get(),
              'Title' : response.css('h1::text').get(),
              'Date' : response.css('time::text').get(),
              'Author(s)' : response.css('a.tone-colour span::text').getall(),
              'Content' : response.css('div.content__article-body p::text').getall()
            }

        #next_page = response.css('a.button::attr(href)').get()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse) 
    
