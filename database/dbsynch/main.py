import argparse
import yaml
from icecream import ic
from dbsynch.task_scheduler import TaskScheduler
from urllib.parse import quote_plus
import pymongo

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

class Synchronized:
    def __init__(self, config_file):
        self.config = self._load_config(config_file)
        self._main_client = None
        self._backup_client = None

    def _load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def _synchronize_collection(self, collection):
        # delete collection from backup database
        backup_db = self._backup_client[self.config['database']]
        main_db = self._main_client[self.config['database']]
        backup_db[collection].drop()
        documents = main_db[collection].find({})
        if documents:
            backup_db[collection].insert_many(documents)

    def synchronize_main_and_backup_databases(self):
        try:
            self._connect_to_dbs()

            backup_db = self._backup_client[self.config['database']]
            main_db = self._main_client[self.config['database']]

            print("Synchronizing databases...")
            self._check_collections(main_db, "main")
            self._check_collections(backup_db, "backup")

            collections = main_db.list_collection_names()
            for collection in collections:
                print(f"Synchronizing collection {collection}...")
                self._synchronize_collection(collection)

            self._check_collections(main_db, "main")
            self._check_collections(backup_db, "backup")
            print("Synchronization completed!")

        finally:
            self._disconnect()

    def _connect_to_dbs(self):
        main_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['host']}:{self.config['port']}"
        print("Connection uri (main database): ", main_db_uri)
        self._main_client = pymongo.MongoClient(main_db_uri, serverSelectionTimeoutMS=10000)
        if self._is_connected(self._main_client):
            print("Connected to MongoDB (main) successfully!")
        else:
            print(f"Error connecting to MongoDB (main) with uri: {main_db_uri}")
            raise Exception(f"Error connecting to MongoDB (main) with uri: {main_db_uri}")
        
        backup_db_uri = f"mongodb://{quote_plus(self.config['user'])}:{quote_plus(self.config['password'])}@{self.config['backup_host']}:{self.config['port']}"
        print("Connection uri (backup database): ", backup_db_uri)
        self._backup_client = pymongo.MongoClient(backup_db_uri, serverSelectionTimeoutMS=10000)
        if self._is_connected(self._backup_client):
            print("Connected to MongoDB (backup) successfully!")
        else:
            print(f"Error connecting to MongoDB (backup) with uri: {backup_db_uri}")
            raise Exception(f"Error connecting to MongoDB (backup) with uri: {backup_db_uri}")

 
    def _disconnect(self):
        if self._main_client:
            self._main_client.close()
            print("Disconnected from main MongoDB")
        if self._backup_client:
            self._backup_client.close()
            print("Disconnected from backup MongoDB")
        
    def _is_connected(self, client):
        try:
            connected = client is not None and client.admin.command('ping')['ok'] == 1
            return connected
        except Exception as e:
            print("Error checking connection to MongoDB: ", e)
            return False
        
    # check all the collections and the number of documents in each collection
    def _check_collections(self, db, uri):
        collections = db.list_collection_names()
        print(f"\nChecking collections in {uri} database...")
        print(f"Found {len(collections)} collections")
        for collection in collections:
            print(f"\tCollection {collection} has {db[collection].count_documents({})} documents")
        print("Check completed!")


        
def main(args):

    ic("Application started!")

    s=Synchronized(args.mongo_config_file)

    scheduler = TaskScheduler()
    h="09:00"
    scheduler.schedule_daily_job(
        h, s.synchronize_main_and_backup_databases
    )
    scheduler.run_all()
    ic(f"Application will run at {h} each day!")
    scheduler.run_scheduler()


if __name__=='__main__':
    args = cli()
    main(args)