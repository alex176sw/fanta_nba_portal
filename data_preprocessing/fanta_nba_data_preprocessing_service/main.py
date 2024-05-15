import yaml
import argparse
from fanta_nba_data_preprocessing_service.preprocessing import standardize, get_teams_statistics
from fanta_nba_data_preprocessing_service.mongo_db_connector import MongoDBConnector
from flask import Flask, request, jsonify

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

@app.route('/get_ml_data/train', methods=['GET'])
def get_ml_data_train():

    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    records = mongo_db.get_games_stats()
    print(records[0])
    # do some processing with home_team and away_team
    records, columns, scaler = standardize(records)

    SCALER = scaler

    return {
        "columns": columns,
        "records": records
    }




@app.route('/get_ml_data/inference', methods=['GET'])
def get_ml_data_inference():    
    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    teams_stats = mongo_db.get_teams_stats()

    home_team = request.args.get('homeTeam')
    away_team = request.args.get('awayTeam')

    home_team_stats, away_team_stats = get_teams_statistics(home_team, away_team, teams_stats)

    if SCALER is None:
        print("TODO: error...")

    records, columns, _ = standardize([home_team_stats, away_team_stats], scaler=SCALER)

    return {
        "columns": columns,
        "records": records
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
