import yaml
import time
import argparse
from fanta_nba_data_preprocessing_service.preprocessing import (
    standardize_train_data, get_teams_statistics, standardize_inference_data
)
from fanta_nba_data_preprocessing_service.mongo_db_connector import MongoDBConnector
from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

args = cli()
app = Flask(__name__)
app.logger.setLevel("DEBUG")
app.logger.info("Starting Data Preprocessing Service")

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

CACHE = {}
TIMEOUT_CACHE_IN_SECONDS = 43200 # 12 hours
LAST_CACHE_UPDATE = None

@app.route('/train', methods=['GET'])
def get_ml_data_train():
    app.logger.info("Train request received")

    global CACHE, LAST_CACHE_UPDATE
    
    # invalidate cache if timeout elapsed
    if LAST_CACHE_UPDATE and time.time() - LAST_CACHE_UPDATE > TIMEOUT_CACHE_IN_SECONDS:
        app.logger.info("Cache timeout elapsed. Invalidating cache")
        CACHE = {}

    if CACHE:
        app.logger.info("Returning cached data")
        return CACHE["data"]
    
    app.logger.info("Fetching data from MongoDB")
    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    records = mongo_db.get_games_stats()
    
    if not records:
        app.logger.info.warning("No data found in MongoDB")
        return {
            "columns": [],
            "records": []
        }
    app.logger.info("Data fetched successfully")
    
    app.logger.info("Standardizing data")
    records, columns, scaler = standardize_train_data(records)

    try:
        mongo_db.save_scaler_params(
            {"mean_": scaler.mean_.tolist(), "scale_": scaler.scale_.tolist()}
        )
    except Exception as e:
        app.logger.error(f"Error saving SCALER params: {e}")

    data = {
        "columns": columns,
        "records": records
    }

    app.logger.info(f"Returning standardized data. Columns: {columns}, Records: {len(records)}. Each record contains {len(records[0])} columns. Example: {records[0]}")
    
    CACHE["data"] = data
    LAST_CACHE_UPDATE = time.time()
    
    return data




@app.route('/inference', methods=['POST'])
def get_ml_data_inference():
    app.logger.info("Inference request received")

    data = request.get_json()
    home_team = data.get('home_team')
    host_team = data.get('host_team')
    app.logger.info(f"Home team: {home_team}, Host team: {host_team}")        

    app.logger.info("Fetching data from MongoDB")
    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)
    teams_stats = mongo_db.get_teams_stats()

    if not teams_stats:
        app.logger.warning("No data found in MongoDB")
        return {
            "columns": [],
            "records": []
        }
    app.logger.info("Data fetched successfully")

    app.logger.info("Getting teams statistics")
    home_team_stats, host_team_stats = get_teams_statistics(home_team, host_team, teams_stats)
    app.logger.info(f"Teams statistics fetched successfully: \n{home_team_stats} \n{host_team_stats}")

    try:
        scaler_params = mongo_db.load_scaler_params()
    except Exception as e:
        app.logger.error(f"Error loading SCALER params: {e}")
        return {
            "columns": [],
            "records": []
        }
    app.logger.info(f"scaler_params: {scaler_params}")

    try:
        scaler = StandardScaler()
        scaler.mean_ = scaler_params["scaler"]["mean_"][-1]
        scaler.scale_ = scaler_params["scaler"]["scale_"][-1]
    except Exception as e:
        app.logger.error(f"Error loading SCALER params: {e}")
        return {
            "columns": [],
            "records": []
        }

    
    app.logger.info("Renaming columns to match the ones used in training data")
    for col, val in home_team_stats.items():
        home_team_stats["home_team_"+col] = val
        del home_team_stats[col]
    for col, val in host_team_stats.items():
        host_team_stats["host_team_"+col] = val
        del host_team_stats[col]

    merged_dict = {**home_team_stats, **host_team_stats}


    app.logger.info("Standardizing data")
    records, columns = standardize_inference_data(merged_dict, scaler=scaler)

    app.logger.info(f"Returning standardized data. Columns: {columns}, Records: {records}")
    return {
        "columns": columns,
        "records": records
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
