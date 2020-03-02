import scrapy
import sys
import html2text 
import pymongo
import dns #required for connecting with SRV
#import collections
import nltk
#from My_spliter import My_spliter
from nltk.stem import WordNetLemmatizer

################################################## My_spliter() #########################################
def My_spliter (a):
    l = []
    for word in a.lower().split():
        word.strip()
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("'","")
        word = word.replace("“","")
        word = word.replace("”","")
        word = word.replace("[","")
        word = word.replace("]","")
        word = word.replace("(","")
        word = word.replace(")","")
        word = word.replace("•","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("?","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        word = wnl.lemmatize(word)
        l.append(word)
    return l
################################################## End My_spliter()########################################## 

################################################### index_generator ######################################################################
stopwords = "ourselves hers between yourself but almost may would again there about once during out very having with hi ha they own an be some for do its yours such into of most itself other off is s am or who as from him each the themselves until below are we these your his through don nor me were her more himself this down should our their while above both up to ours had she all no when at any before them same and been have in will on does yourselves then that because what over why so can did not now under he you herself has ha just where too only myself which those i after few whom t being if theirs my against a by doing it how further was wa here than also said could – _ - "
stopwords = stopwords.split()
wnl = WordNetLemmatizer()
def tags(a):
    #stopwords = set(line.strip() for line in open('stopwords.txt'))
    #stopwords = stopwords.union(set(['mr','mrs','one','two','the','of','to']))
    
    # Instantiate a dictionary, and for every word in the file, 
    # Add to the dictionary if it doesn't exist. If it does, increase the count.
    wordcount = {}
    myIdx = []
    l = My_spliter(a)
    for word in l:
        if word not in stopwords:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
                
    # Print most common word
    #n_print = int(input("How many most common words to print: "))
    n_print  = int(10)
    #print("\nThe {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    for word, count in word_counter.most_common(n_print):
        myIdx.append(word) #append([word,count])
    return myIdx
        #print(word, ": ", count)
        #yield word,count
######################################################### End index_generator() ##########################################################

########################################################## Principal class ############################################################
class MySpider(scrapy.Spider):
    name = 'guardian'
    #allowed_domains = ['theguardian.com']

    catg = ''
    limit = 2
    #categories = ["world","environment","science","cities","global-development","football","technology","business"]
    def __init__(self, category=None, pgLimit=2, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.theguardian.com/%s?page=1' % category]
        global catg 
        catg = category

        global limit
        limit = pgLimit
    ############################################### establish the connection to mongodb ############################################
        cnx = pymongo.MongoClient("mongodb+srv://guest:guest@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
        db = cnx['GemoDB']
        global collc
        collc = db[catg]
    ####################################################################################################################################

    def parse(self, response):
        #htmt2text to get the plain text
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        
        if response.css('div.content__article-body p').extract() != [] :
            #Get informations relevant to the news story
            h_title = ((converter.handle(str(response.css('h1').get())).replace("#", '').strip()).replace("\n\n", '')).replace("\n", ' ')
            h_date = response.css('time::text').get()
            h_author = response.css('div.meta__contact-wrap p.byline').extract_first()
            h_body = response.css('div.content__article-body p').extract()
            Content_tags = tags(((str((converter.handle(str(h_body))).strip())).replace("\n\n",'')).replace("\n",' ').replace("[]",''))

            stopwords.extend(Content_tags)
            splited_title = My_spliter(h_title)
            for word in splited_title:
                if word not in (stopwords):
                    Content_tags.append(word)

            #Return these informations
            article = {
            'URL' : "https://www.theguardian.com"+response.css('html::attr(data-page-path)').get(),
            'Title' : h_title,
            'Date' : h_date.strip(),
            'Author(s)' : (str((converter.handle(str(h_author))))).strip().replace("\n",' '),
            'Content' : ((str((converter.handle(str(h_body))).strip())).replace("\n\n",'')).replace("\n",' '),
            'Content_tags' : Content_tags
            }
            #yield article
            collc.insert_one(article)        
        #response.xpath('//a[@class="u-faux-block-link__overlay js-headline-text"]/@href').extract() or response.css('a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall()
        for article_url in response.css('section.fc-container.fc-container--tag a.u-faux-block-link__overlay.js-headline-text::attr(href)').getall():
            yield scrapy.Request(response.urljoin(article_url), self.parse)
        
        
        next_page = response.css('a.button.button--small.button--tertiary.pagination__action--static[rel="next"]::attr(href)').get()
        if next_page == ('https://www.theguardian.com/%s?page=%s' % (catg, limit)):
            sys.exit("Limit reached !")
        yield scrapy.Request(response.urljoin(next_page), self.parse)
########################################################## End Principal class ############################################################
#testing1.json: For performance reasons, document symbols have been limited to 5000 items.
#Use setting 'json.maxItemsComputed' to configure the limit.
