import time
import requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from database import Database

class InferenceService:
    def __init__(self, args):
        self.db = Database(args.mongo_config_file)
        self.data_preprocessing_service_url = f"http://flask-app-preprocessing:5000"

    def load_model(self, model_type, model_params):
        if model_type == "logistic-regression":
            model = LogisticRegression()
            model.set_params(**model_params)
            return model
        # Add other model types here as needed
        return None

    def fetch_encoded_data(self, home_team, away_team):
        response = requests.post(self.data_preprocessing_service_url + '/inference', json={"home_team": home_team, "away_team": away_team})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch encoded data from preprocessing service")



    def run(self):
        while True:
            inference_request = self.db.get_next_inference_request()

            if inference_request:
                self.db.remove_inference_request(inference_request["_id"])

                print(f"New inference request: {inference_request}")

                home_team = inference_request["home_team"]
                away_team = inference_request["host_team"]
                trained_model = inference_request["trained_model"]

                try:
                    print("Get encoded data from preprocessing service")
                    encoded_data = self.fetch_encoded_data(home_team, away_team)
                    print("Get model from database")
                    model_record = self.db.get_trained_model(trained_model)
                    print("Load model")
                    model = self.load_model(model_record["model_type"], model_record["model_params"])
                    print("Perform inference")
                    inference_result = self.perform_inference(model, encoded_data)
                    inference_result["timestamp"] = time.time()
                    print(f"Performed inference for model: {trained_model}")
                    inference_result["message"] = "Inference successful"
                except Exception as e:
                    inference_result = {
                        "home_team_win_prob": None,
                        "host_team_win_prob": None,
                        "message" : f"Error during inference: {e}",
                        "timestamp": time.time()
                    }
                    print(f"Error during inference: {e}")

                self.db.save_inference_result(inference_result)

            time.sleep(10)  # Wait for 10 seconds before checking for new requests


    def perform_inference(self, model, encoded_data):
        X = np.array([encoded_data["features"]])
        probabilities = model.predict_proba(X)[0]
        return {
            "home_team_win_prob": probabilities[0],
            "host_team_win_prob": probabilities[1]
        }