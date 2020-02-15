import scrapy
from postscrape.items import PostscrapeItem
import pymongo
from scrapy import settings
from scrapy.exceptions import DropItem
from scrapy.utils import log

################################################# MongoDBPipeline ##############################################

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient("mongodb+srv://CHEA:started@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
        db = connection.GemoDB
        self.collection = Gemo
    
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Post added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
#################################################################################################################


#################################################################################################################

class PostsSpider(scrapy.Spider):
    name = 'itm'
    start_urls = [
                    'https://blog.scrapinghub.com/'
                ]
    
    def parse(self, response):
        for post in response.css('div.post-item'):
            item = PostscrapeItem()
            
            item['Title'] = post.css('.post-header h2 a::text')[0].get()
            item['Date'] = post.css('.post-header a::text')[1].get()
            item['Author'] = post.css('.post-header a::text')[2].get()
            
            yield item 
        
        #next_page = response.css('a.next-posts-link::attr(href)').get()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse) 
    
