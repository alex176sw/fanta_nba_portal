import yaml
import argparse
from fanta_nba_data_preprocessing_service.preprocessing import standardize
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

@app.route('/get_ml_data/train', methods=['GET'])
def get_ml_data_train():
    print("h1")
    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    records = mongo_db.get_games_stats(load_config(args.mongo_config_file)["collection"])

    # do some processing with home_team and away_team
    records, columns, scaler_mean, scaler_scale = standardize(records)


    return {
        "columns": columns,
        "records": records,
        "scaler_params": {
            "mean": scaler_mean,
            "scale": scaler_scale
        }
    }

 


@app.route('/get_ml_data/inference', methods=['GET'])
def get_ml_data_inference():    
    mongo_db = MongoDBConnector(config_file=args.mongo_config_file)

    #doc = mongo_db.get_teams_games_stats(load_config(args.mongo_config_file)["collection"])

    home_team = request.args.get('homeTeam')
    away_team = request.args.get('awayTeam')


    # do some processing with home_team and away_team
    ml_inference_data = {'result': "TODO"}
    return jsonify(ml_inference_data)

 



if __name__ == '__main__':
    app.run(debug=True)
