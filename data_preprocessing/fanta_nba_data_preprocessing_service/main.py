import argparse
from data_preprocessing.mongo_db_connector import MongoDBConnector
from flask import Flask, request, jsonify

from fanta_nba_data_preprocessing_service.
def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

args = cli()
app = Flask(__name__)

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    # Receive request data from Node.js
    request_data = request.json
    
    MongoDBConnector(config_file=args.mongo_config_file),

    # Example: Query MongoDB based on request data
    mongo_data = query_mongodb(request_data)

    # Example: Preprocess the data
    processed_data = preprocess_data(mongo_data)
    
    # Return processed data to Node.js
    return jsonify(processed_data)



if __name__ == '__main__':
    app.run(debug=True)
