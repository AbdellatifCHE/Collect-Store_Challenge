import scrapy
from postscrape.items import PostscrapeItem
from postscrape.items import PostscrapeItem
import pymongo
import dns #required for connecting with SRV
import html2text
################################################# connection to mongodb ##############################################

cnx = pymongo.MongoClient("mongodb+srv://CHEA:started@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
db = cnx['GemoDB']
collc = db['test1']
####################################################################################################################

class PostsSpider(scrapy.Spider):
    name = 'posts'
    #allowed_domains = ["bbc.com"]

    start_urls = [
                    'https://www.theguardian.com/science?page=1'
                    #'https://blog.scrapinghub.com/'
                ]
    
    def parse(self, response):
        #for post in response.css('div.post-item'):
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        h_title = response.css('h1').get()
        h_date = response.css('time::text').get()
        h_author = response.css('div.meta__contact-wrap p').extract_first()
        item = PostscrapeItem()
        
        item['Title'] : ((converter.handle(str(h_title)).replace("#", '').strip()).replace("\n\n", '')).replace("\n", ' ')#post.css('.post-header h2 a::text')[0].get()
        item['Date'] : h_date.strip()#post.css('.post-header a::text')[1].get()
        item['Author'] : (str((converter.handle(str(h_author))))).strip()#post.css('.post-header a::text')[2].get() 
        
        yield item
            #collc.insert_one(item)
        #next_page = response.css('a.next-posts-link::attr(href)').get()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse) 
    
