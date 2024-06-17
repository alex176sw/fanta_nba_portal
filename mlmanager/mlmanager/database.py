import yaml
import pymongo
from bson.objectid import ObjectId
import os
from urllib.parse import quote_plus

class Database:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        main_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['host']}"
        self.client = pymongo.MongoClient(main_db_uri, port=self.config['port'], serverSelectionTimeoutMS=10000)
        self.db = self.client[self.config['database']]

    def get_trained_models(self):
        models_collection = self.db['trained_models']
        return list(models_collection.find({}, {'_id': 0}))

    def get_training_results(self):
        results_collection = self.db['training_results']
        return list(results_collection.find({}, {'_id': 0}))
        
    def get_inference_results(self):
        results_collection = self.db['inference_results']
        return list(results_collection.find({}, {'_id': 0}))

    def add_trained_model(self, model):
        models_collection = self.db['trained_models']
        models_collection.insert_one(model)

    def add_inference_result(self, result):
        results_collection = self.db['inference_results']
        results_collection.insert_one(result)

    def get_train_queue_length(self):
        queue_collection = self.db['train_queue']
        return queue_collection.count_documents({})

    def get_inference_queue_length(self):
        queue_collection = self.db['inference_queue']
        return queue_collection.count_documents({})

    def add_to_train_queue(self, model_type):
        queue_collection = self.db['train_queue']
        queue_collection.insert_one({"model_type": model_type})

    def add_to_inference_queue(self, home_team, away_team, trained_model):
        queue_collection = self.db['inference_queue']
        queue_collection.insert_one({
            "home_team": home_team,
            "away_team": away_team,
            "trained_model": trained_model
        })
