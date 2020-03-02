import pymongo
import dns #required for connecting with SRV
from My_spliter import My_spliter

#Establishing cnx to the mongoDB server
cnx = pymongo.MongoClient("mongodb+srv://guest:guest@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
db = cnx['GemoDB']

categories = ["world","environment","science","cities","global-development","football","technology","business"]

keywords = input("What do you want to search for ?\n")
keywords = My_spliter(keywords)
resp = []
#Create an index for the collection
def api():
    for ctg in categories:
        collc = db[ctg]
        collc.create_index([("Content_tags", 1)])

        rslt = collc.find({"Content_tags": {"$all": keywords }})
        #if rslt.count() != 0 :
        for doc in rslt:
            resp.append(doc)
    return resp

resp = api()
#Create a file to store the search results
f= open("search_results.txt","w+")
f.write("Search results:\n")
for doc in resp:
    f.write("Title: %s, " % doc['Title'])
    f.write("Date: %s, " % doc['Date'])
    f.write("Author(s): %s, " % doc['Author(s)'])
    f.write("URL: %s \n" % doc['URL'])
f.close()
