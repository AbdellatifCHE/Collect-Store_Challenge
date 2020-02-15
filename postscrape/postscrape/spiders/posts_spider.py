import scrapy
from postscrape.items import PostscrapeItem

import pymongo
import dns #required for connecting with SRV

################################################# connection to mongodb ##############################################

cnx = pymongo.MongoClient("mongodb+srv://CHEA:started@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
db = cnx['GemoDB']
collc = db['test1']
####################################################################################################################

class PostsSpider(scrapy.Spider):
    name = 'posts'
    #allowed_domains = ["bbc.com"]

    start_urls = [
                    'https://blog.scrapinghub.com/'
                ]
    
    def parse(self, response):
        for post in response.css('div.post-item'):
            item = {
            'Title' : post.css('.post-header h2 a::text')[0].get(),
            'Date' : post.css('.post-header a::text')[1].get(),
            'Author' : post.css('.post-header a::text')[2].get()
            }
            #collc.insert_one(item)
        #next_page = response.css('a.next-posts-link::attr(href)').get()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse) 
    
