import os
import pymongo
import pickle
from urllib.parse import quote_plus

class Database:
    def __init__(self, config):
        self.config = config
        main_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['host']}"
        self.client = pymongo.MongoClient(main_db_uri, port=self.config['port'], serverSelectionTimeoutMS=2000)
        self.db = self.client[self.config['database']]

    def get_next_training_request(self):
        return self.db['train_queue'].find_one()

    def remove_training_request(self, request_id):
        self.db['train_queue'].delete_one({'_id': request_id})

    def save_trained_model(self, timestamp, model_type, model):
        pickled_model = pickle.dumps(model)
        model_params = model.get_params()
        self.db['trained_models'].insert_one({
            "model_type": model_type,
            "timestamp": timestamp,
            "pickled_model": pickled_model,
            "model_params": model_params
        })

    def save_training_result(self, result):
        self.db['training_results'].insert_one(result)