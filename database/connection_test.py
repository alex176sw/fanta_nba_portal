from pymongo import MongoClient

# Define MongoDB connection details
mongo_host = 'localhost'  # Docker host IP address
mongo_port = 27017  # Default MongoDB port
mongo_database = 'fantanba'  # Name of the MongoDB database
mongo_collection = 'matches'  # Name of the MongoDB collection

def connect_to_mongodb(host, port, database):
    try:
        # Create a MongoDB client
        client = MongoClient(host, port)
        
        # Access the specified database
        db = client[database]
        
        print("Connected to MongoDB successfully!")
        return db
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None

def main():
    # Connect to MongoDB
    db = connect_to_mongodb(mongo_host, mongo_port, mongo_database)

    if db is not None:
        # Access a collection in the database
        collection = db[mongo_collection]
        
        # Example: Inserting a document into the collection
        document = {"home_team": "Lakers", "away_team": "Chicago Bulls"}
        collection.insert_one(document)
        print("Document inserted successfully!")
        
        # Example: Querying documents from the collection
        documents = collection.find({})
        for doc in documents:
            print(doc)
        
        # Close MongoDB connection
        db.client.close()
        print("MongoDB connection closed.")

if __name__ == "__main__":
    main()
