import yaml
import time
import pickle
import requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError
from database import Database
import logging

class InferenceService:
    def __init__(self, args):
        with open(args.config_file, 'r', encoding="UTF-8") as f:
            self.config = yaml.safe_load(f)
        self.db = Database(self.config)
        self.data_preprocessing_service_url = self.config['preprocessing-service-url']




    def run(self):
        logging.info("Inference service is running!!")

        while True:

            try:
                inference_request = self.db.get_next_inference_request()
            except Exception as e:
                self._save_inference_results("Error during fetching inference request: ", e)
                continue


            if inference_request:

                try:
                    self.db.remove_inference_request(inference_request["_id"])
                except Exception as e:
                    self._save_inference_results("Error during removing inference request: ", e)
                    continue

                logging.info(f"New inference request: {inference_request}")

                home_team = inference_request["home_team"]
                host_team = inference_request["host_team"]
                trained_model = inference_request["trained_model"]

                logging.info("Get encoded data from preprocessing service")
                try:
                    encoded_data = self.fetch_encoded_data(home_team, host_team)
                except Exception as e:
                    self._save_inference_results(f"Error during fetching encoded data with home_team={home_team} and host_team={host_team}: ", e)
                    continue
                logging.info(f"Encoded data: {encoded_data}")

                logging.info("Get model from database")
                try:
                    model_record = self.db.get_trained_model(trained_model)
                except Exception as e:
                    self._save_inference_results(f"Error during fetching model record {trained_model} from database: ", e)
                    continue

                if model_record is None:
                    self._save_inference_results(f"Model record of {trained_model} not found in database", None)
                    continue

                logging.info("Load model")
                try:       
                    model = self.load_model(model_record["pickled_model"])
                except Exception as e:
                    self._save_inference_results(f"Error during loading model {model_record}: ", e)
                    continue

                if model is None:
                    self._save_inference_results(f"Model {model_record} not found", None)
                    continue

                try:
                    check_is_fitted(model)
                except NotFittedError as exc:
                    self._save_inference_results(f"Model {model_record} is not fitted yet. {exc}", None)
                    continue
                
                input_X = np.array([encoded_data["records"]]).flatten().reshape(1, -1)
                logging.info(f"X: {input_X.shape} {input_X}")



                logging.info("Perform inference")
                try:
                    inference_result = self.perform_inference(model, input_X)
                    inference_result["timestamp"] = time.time()
                    inference_result["message"] = "Inference successful"
                    logging.info(f"Performed inference for model: {trained_model}. Results: {inference_result}")
                except Exception as e:
                    self._save_inference_results("Error during inference: ", e)
                    continue

                self.db.save_inference_result(inference_result)

            time.sleep(self.config['sleep_time'])  # Wait before checking for new requests



    def load_model(self, pickled_model):
        return pickle.loads(pickled_model)

    def fetch_encoded_data(self, home_team, host_team):
        response = requests.post(
            self.data_preprocessing_service_url + '/inference', 
            json={"home_team": home_team, "host_team": host_team},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch encoded data from preprocessing service: {response.json()}")


    def _save_inference_results(self, message: str, e: Exception):
        logging.info(f"Error during inference: {message} {e}")
        inference_result = {
            "home_team_win_prob": None,
            "host_team_win_prob": None,
            "message" : f"Error during inference: {message} {e}",
            "timestamp": time.time()
        }
        try:
            self.db.save_inference_result(inference_result)
        except Exception as e:
            logging.error(f"Error during saving inference result: {e}")

    def perform_inference(self, model, X):
        probabilities = model.predict_proba(X)[0]
        return {
            "home_team_win_prob": probabilities[0],
            "host_team_win_prob": probabilities[1]
        }
