import os
import pymongo
import yaml
from pymongo import MongoClient
from urllib.parse import quote_plus

class Database:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        main_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['host']}"
        self.client = pymongo.MongoClient(main_db_uri, port=self.config['port'], serverSelectionTimeoutMS=2000)
        self.db = self.client[self.config['database']]

    def get_next_inference_request(self):
        return self.db['inference_queue'].find_one()

    def remove_inference_request(self, request_id):
        self.db['inference_queue'].delete_one({'_id': request_id})

    def get_trained_model(self, model_name):
        return self.db['trained_models'].find_one({"model_type": model_name}, {'_id': 0})

    def save_inference_result(self, result):
        self.db['inference_results'].insert_one(result)
