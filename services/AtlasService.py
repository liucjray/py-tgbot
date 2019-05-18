from pymongo import MongoClient
from config.config import *


class AtlasService:
    config = get_config()
    prepares = []
    collection = None

    def __init__(self, settings):
        self.settings = settings
        self.collection = self.get_collection(self.settings['collection'])

    def get_collection(self, collection):
        client = MongoClient(self.config['MONGODB']['CONNECTION_ATLAS'])
        mongo_collection = client.get_database(self.config['MONGODB']['DB'])[collection]
        return mongo_collection

    def write_prepare(self, updates):
        for update in updates:
            # 統一轉換為 dict
            if not isinstance(update, dict):
                update = update.to_dict()
                
            # 判斷後寫入
            if int(update['message']['chat']['id']) == int(self.settings['chat_id']):
                self.prepares.append(update)

    def write(self, updates):
        try:
            self.write_prepare(updates)
            self.collection.insert_many(self.prepares, ordered=False)
        except Exception as e:
            print(__file__, e)

    def get_data_deleted(self):
        return self.collection.find({'is_deleted': None})

    def delete(self, where={}, update={}):
        self.collection.update_one(where, update)
