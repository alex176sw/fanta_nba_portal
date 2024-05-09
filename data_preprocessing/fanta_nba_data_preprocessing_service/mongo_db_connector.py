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

    def insert_data(self, data: dict):
        client = self._connect_to_db()
        collection = client[self.config["collection"]]
        result = collection.insert_one(data)
        print("Data inserted with ID:", result.inserted_id)

    def get_games_stats(self):
        print(f"Fetching from collection {self.config['games_stats_collection_name']}")
        return self.get_most_recent_doc(self.config['games_stats_collection_name'])

    def get_teams_stats(self):
        print(f"Fetching from collection {self.config['teams_stats_collection_name']}")
        return self.get_most_recent_doc(self.config['teams_stats_collection_name'])

    def get_most_recent_doc(self, collection_name):
        client = self._connect_to_db()
        collection = client[collection_name]
        most_recent_doc = collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        print(f"Found {len(most_recent_doc)} records")
        most_recent_doc.pop("_id")
        key = list(most_recent_doc.keys())[0]
        return most_recent_doc[key]    