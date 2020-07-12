import os
import pymongo

db_client = pymongo.MongoClient(host=os.getenv('DB_HOST'),
                                port=int(os.getenv('DB_PORT')))
db = db_client.twitter
