import time
import requests
import numpy as np
from sklearn.linear_model import LogisticRegression
from database import Database

class TrainerService:
    def __init__(self, args):
        self.db = Database(args.mongo_config_file)
        self.data_preprocessing_service_url = f"http://flask-app-preprocessing:5000"

    def fetch_data(self):
        response = requests.get(self.data_preprocessing_service_url + '/train')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from preprocessing service")

    def run(self):
        while True:
            training_request = self.db.get_next_training_request()

            if training_request:
                self.db.remove_training_request(training_request["_id"])


                print(f"New inference request: {training_request}")

                model_type = training_request["model_type"]

                training_result = {
                    "model_type": model_type,
                    "timestamp": time.time()
                }
                try:
                    print("Get data from preprocessing service")
                    data = self.fetch_data()
                    if data:
                        print("Train the model")
                        model_params = self.train_model(model_type, data)
                        print("Save the model to database")
                        self.db.save_trained_model(model_type, model_params)
                        print(f"Trained and saved model of type: {model_type}")
                        training_result["message"] = "Model trained successfully"
                except Exception as e:
                    print(f"Error during training: {e}")
                    training_result["message"] = f"Error during training: {e}"

                self.db.save_training_result(training_result)

            time.sleep(10)  # Wait for 10 seconds before checking for new requests

    def train_model(self, model_type, data):
        """
        The first column is the target y
        The remaining columns are the features X
        """
        data = np.array(data["records"])

        X = data[:, 0]
        y = data[:, 1:]

        if model_type == "logistic-regression":

            model = LogisticRegression()
            model.fit(X, y)
            print(f"Model trained with parameters: {model.get_params()}")
            return model.get_params()
        else:
            print(f"Model type {model_type} not supported")
        # Add other model types here as needed
        return None