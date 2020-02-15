import scrapy
import sys
import html2text 

import pymongo
import dns #required for connecting with SRV

class MySpider(scrapy.Spider):
    name = 'testing'
    #allowed_domains = ['theguardian.com']

    catg = ''

    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.theguardian.com/%s?page=1' % category]
        global catg 
        catg = category
    ################################################# establish the connection to mongodb ##############################################
        cnx = pymongo.MongoClient("mongodb+srv://CHEA:started@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
        db = cnx['GemoDB']
        global collc
        collc = db[catg]
    ####################################################################################################################################


    #categories = ["world","environment","science","cities","global-development","football","technology","business"]
    #start_urls = [
    #                'https://www.theguardian.com/science?page=1'
    #            ]

    def parse(self, response):
        #Use htmt2text to get the plain text
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        
        if  response.css('h1::text').get() != ' ':
                #Get informations relevant to the news story
                h_title = response.css('h1').get()
                h_date = response.css('time::text').get()
                h_author = response.css('div.meta__contact-wrap p').extract_first()
                h_body = response.css('div.content__article-body p').extract()

                #Return these informations
                article = {
                'URL' : "https://www.theguardian.com"+response.css('html::attr(data-page-path)').get(),
                'Title' : ((converter.handle(str(h_title)).strip()).replace("\n\n", '')).replace("\n", ' '),
                'Date' : h_date.strip(),
                'Author(s)' : (str((converter.handle(str(h_author))))).strip(),
                'Content' : ((str((converter.handle(str(h_body))).strip())).replace("\n\n",'')).replace("\n",' ')
                            
                }
                collc.insert_one(article)        
        #response.xpath('//a[@class="u-faux-block-link__overlay js-headline-text"]/@href').extract() or response.css('a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall()
        for article_url in response.css('section.fc-container.fc-container--tag a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall():
            yield scrapy.Request(response.urljoin(article_url), self.parse)
        
        
        #next_page = response.css('a.button.button--small.button--tertiary.pagination__action--static[rel="next"]::attr(href)').get()
        #if next_page == ('https://www.theguardian.com/%s?page=101' % catg):
        #    sys.exit("Limit reached !")
        #yield scrapy.Request(response.urljoin(next_page), self.parse)
             
#testing1.json: For performance reasons, document symbols have been limited to 5000 items.
#Use setting 'json.maxItemsComputed' to configure the limit.
