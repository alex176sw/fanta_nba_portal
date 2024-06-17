import yaml
import time
import argparse
from fanta_nba_data_preprocessing_service.preprocessing import (
    standardize_train_data, get_teams_statistics, standardize_inference_data
)
from fanta_nba_data_preprocessing_service.mongo_db_connector import MongoDBConnector
from flask import Flask, request, jsonify
from pprint import pprint

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

args = cli()
app = Flask(__name__)

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

SCALER = None
CACHE = {}
TIMEOUT_CACHE_IN_SECONDS = 43200 # 12 hours
LAST_CACHE_UPDATE = None

@app.route('/train', methods=['GET'])
def get_ml_data_train():
    global SCALER, CACHE, LAST_CACHE_UPDATE
    
    # invalidate cache if timeout elapsed
    if LAST_CACHE_UPDATE and time.time() - LAST_CACHE_UPDATE > TIMEOUT_CACHE_IN_SECONDS:
        CACHE = {}

    if CACHE:
        return CACHE["data"]
    

    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    records = mongo_db.get_games_stats()
    
    if not records:
        return {
            "columns": [],
            "records": []
        }
    
    records, columns, scaler = standardize_train_data(records)
    

    data = {
        "columns": columns,
        "records": records
    }
    
    print(f"Updating CACHE with columns: {columns} and data: {len(records)} records. Each record contains {len(records[0])} columns. Example: {records[0]}")
    SCALER = scaler
    CACHE["data"] = data
    LAST_CACHE_UPDATE = time.time()
    
    return data




@app.route('/inference', methods=['GET'])
def get_ml_data_inference():
    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    teams_stats = mongo_db.get_teams_stats()

    if not teams_stats:
        return {
            "columns": [],
            "records": []
        }

    home_team = request.args.get('homeTeam')
    away_team = request.args.get('awayTeam')

    home_team_stats, away_team_stats = get_teams_statistics(home_team, away_team, teams_stats)

    if SCALER is None:
        print("TODO: error...")
        return {
            "columns": [],
            "records": []
        }
    
    print("Renaming columns (col_name => home_team_col_name) to match the ones used in training data")
    for col, val in home_team_stats.items():
        home_team_stats["home_team_"+col] = val
        del home_team_stats[col]
    for col, val in away_team_stats.items():
        away_team_stats["away_team_"+col] = val
        del away_team_stats[col]

    merged_dict = {**home_team_stats, **away_team_stats}

    pprint(merged_dict)

    records, columns = standardize_inference_data(merged_dict, scaler=SCALER)

    pprint(records)
    return {
        "columns": columns,
        "records": records
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
