import yaml
import time
import requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError
import logging
try:
    from trainer.database import Database
except Exception as e:
    from database import Database

class TrainerService:
    def __init__(self, args):
        with open(args.config_file, 'r', encoding="UTF-8") as f:
            self.config = yaml.safe_load(f)
        self.db = Database(self.config)
        self.data_preprocessing_service_url = self.config['preprocessing-service-url']

    def run(self):
        while True:
            time.sleep(self.config['sleep_time'])  # Wait before checking for new requests

            try:
                training_request = self.db.get_next_training_request()
            except Exception as e:
                self._save_training_results("Error during fetching training request", e, {})
                continue

            if training_request is None:
                logging.info("No training request found")
                continue

            try:
                self.db.remove_training_request(training_request["_id"])
            except Exception as e:
                self._save_training_results("Error during removing training request", e, {})
                continue

            logging.info(f"New inference request: {training_request}")


            model_type = training_request["model_type"]
            timestamp = time.time()
            training_result = {
                "model_type": model_type,
                "timestamp": timestamp
            }

            try:
                logging.info("Get data from preprocessing service")
                data = self.fetch_data()
            except Exception as e:
                self._save_training_results("Error during fetching data", e, training_result)
                continue

            if not data:
                logging.info("No data fetched")
                self._save_training_results("No data fetched", None, training_result)
                continue

            try:
                logging.info("Train model")
                model = self.train_model(model_type, data)
            except Exception as e:
                self._save_training_results("Error during training", e, training_result)
                continue
            
            try:
                check_is_fitted(model)
            except NotFittedError as exc:
                self._save_training_results(f"Model {model} is not fitted yet. {exc}", None, training_result)
                continue

            try:
                logging.info("Save trained model")
                self.db.save_trained_model(timestamp, model_type, model)
            except Exception as e:
                self._save_training_results("Error during saving model", e, training_result)
                continue

            training_result["message"] = "Model trained successfully"
            self.db.save_training_result(training_result)


    def train_model(self, model_type, data):
        """
        The first column is the target y
        The remaining columns are the features X
        """
        data = np.array(data["records"])

        if len(data) == 0:
            raise Exception("No data to train the model")

        X = data[:, 1:]
        y = data[:, 0]

        if model_type == "logistic-regression":

            model = LogisticRegression()
            model.fit(X, y)
            logging.info(f"Model trained with parameters: {model.get_params()}")
            return model
        else:
            logging.warning(f"Model type {model_type} not supported")
            raise ValueError(f"Model type {model_type} not supported")
        # Add other model types here as needed
        return None


    def _save_training_results(self, message: str, e: Exception, training_result: dict):
        logging.info(f"Error during training: {message} {e}")
        training_result["message"] = f"Error during inference: {message} {e}"
        if "timestamp" not in training_result:
            training_result["timestamp"] = time.time()
        if "model_type" not in training_result:
            training_result["model_type"] = "unknown"
        
        try:
            self.db.save_training_result(training_result)
        except Exception as e:
            logging.error(f"Error during saving training result: {e}")

    def fetch_data(self):
        response = requests.get(self.data_preprocessing_service_url + '/train')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from preprocessing service")