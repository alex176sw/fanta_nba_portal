import os
import yaml
import pymongo
from urllib.parse import quote_plus

class Database:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        main_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['host']}"
        self.client = pymongo.MongoClient(main_db_uri, port=self.config['port'], serverSelectionTimeoutMS=2000)
        self.db = self.client[self.config['database']]

    def get_next_training_request(self):
        return self.db['train_queue'].find_one()

    def remove_training_request(self, request_id):
        self.db['train_queue'].delete_one({'_id': request_id})

    def save_trained_model(self, model_type, model_params):
        self.db['trained_models'].insert_one({
            "model_type": model_type,
            "model_params": model_params
        })

    def save_training_result(self, result):
        self.db['training_results'].insert_one(result)