import pymongo
import dns #required for connecting with SRV
import pymongo
cnx = pymongo.MongoClient("mongodb+srv://CHEA:started@mycluster-uykvf.azure.mongodb.net/GemoDB?retryWrites=true&w=majority")
db = cnx['GemoDB']
collc = db['test1']

data1 = {"name":"blabla","src":"vscode"}
data2 = {}

#collc.insert_one(data1)
