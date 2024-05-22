import yaml
import pymongo
from urllib.parse import quote_plus

class MongoDBConnector:
    def __init__(self, config_file):
        self.config = self._load_config(config_file)
        self._client = None
        self._db = None
        self._connect_to_db()

    def _load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def _is_connected(self):
        print("Checking if connected to MongoDB...")
        try:
            connected = self._client is not None and self._client.is_primary
            return connected
        except Exception as e:
            print("Error checking connection to MongoDB: ", e)
            return False
        
    def _connect_to_db(self):
        main_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['host']}"
        print("Connection uri (main database): ", main_db_uri)

        self._client = pymongo.MongoClient(main_db_uri, port=self.config['port'], serverSelectionTimeoutMS=1000)
        self._db = self._client[self.config['database']]

        if self._is_connected():
            print("Connected to MongoDB successfully!")
            return
        else:
            print("Connecting to backup database")            
            backup_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['backup_host']}"
            print("Connection uri (backup database): ", backup_db_uri)
            self._client = pymongo.MongoClient(backup_db_uri, port=self.config['backup_port'], serverSelectionTimeoutMS=1000)
            self._db = self._client[self.config['database']]
            if self._is_connected():
                print("Connected to MongoDB (backup) successfully!")
                return
            else:
                print("Error connecting to MongoDB")
                raise Exception("Error connecting to MongoDB")
        

    def insert_data(self, data: dict):
        if not self._is_connected():
            self._connect_to_db()
        collection = self._db[self.config["collection"]]
        result = collection.insert_one(data)
        print("Data inserted with ID:", result.inserted_id)

    def get_games_stats(self):
        print(f"Fetching from collection {self.config['games_stats_collection_name']}")
        return self.get_most_recent_doc(self.config['games_stats_collection_name'])

    def get_teams_stats(self):
        print(f"Fetching from collection {self.config['teams_stats_collection_name']}")
        return self.get_most_recent_doc(self.config['teams_stats_collection_name'])

    def get_most_recent_doc(self, collection_name):
        if not self._is_connected():
            self._connect_to_db()
        collection = self._db[collection_name]
        most_recent_doc = collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        if not most_recent_doc:
            print(f"No documents found!")
            return None
        print(f"Found {len(most_recent_doc)} records")
        most_recent_doc.pop("_id")
        key = list(most_recent_doc.keys())[0]
        return most_recent_doc[key]
    

if __name__=='__main__':
    m = MongoDBConnector("config/default.yaml")
    m.get_games_stats()
    m.get_teams_stats()