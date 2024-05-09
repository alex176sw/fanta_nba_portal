import yaml
import pymongo

class MongoDBConnector:
    def __init__(self, config_file):
        self.config = self._load_config(config_file)

    def _load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def _connect_to_db(self):
        client = pymongo.MongoClient(self.config['host'], self.config['port'])
        return client[self.config['database']]

    def insert_data_into_teams_stats_collection(self, data: dict):
        self.insert_data_into_collection(data, self.config["teams_stats_collection_name"])

    def insert_data_into_games_collection(self, data: dict):
        self.insert_data_into_collection(data, self.config["games_stats_collection_name"])

    def insert_data_into_collection(self, data, collection):
        client = self._connect_to_db()
        collection = client[collection]
        result = collection.insert_one(data)
        print(f"Data inserted in collection {collection} with ID {result.inserted_id}")
