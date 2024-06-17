import argparse
import yaml
from flask import Flask, request, jsonify
from mlmanager.database import Database

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()


app = Flask(__name__)
args = cli()
db = Database(args.mongo_config_file)

@app.route('/overview', methods=['GET'])
def overview():
    trained_models = db.get_trained_models()
    train_queue_length = db.get_train_queue_length()
    inference_queue_length = db.get_inference_queue_length()
    inference_results = db.get_inference_results()
    training_results = db.get_training_results()

    response = {
        "trainedModels": trained_models,
        "trainQueueLength": train_queue_length,
        "inferenceQueueLength": inference_queue_length,
        "inferenceResults": inference_results,
        "trainingResults": training_results
    }
    return jsonify(response)

@app.route('/train', methods=['POST'])
def train():
    model_type = request.json.get('modelType')
    db.add_to_train_queue(model_type)
    return jsonify({"message": "Model training request added to queue."})

@app.route('/inference', methods=['POST'])
def inference():
    home_team = request.json.get('homeTeam')
    away_team = request.json.get('awayTeam')
    trained_model = request.json.get('trainedModel')
    db.add_to_inference_queue(home_team, away_team, trained_model)
    return jsonify({"message": "Inference request added to queue."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
