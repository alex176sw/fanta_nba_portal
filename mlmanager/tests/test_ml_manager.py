import pytest
import requests
from mlmanager import main

BASE_URL = 'http://localhost:5001'

sample_model_data = {
    "model_name": "LogisticRegression",
    "model_params": {
        "C": 1.0,
        "solver": "liblinear"
    }
}

@pytest.fixture
def setup():
    # Perform setup steps if needed
    # For example, initialize the database with sample data
    yield
    # Teardown steps if needed
    # For example, clean up database after tests

def test_train_model(setup):
    # Simulate /train endpoint
    url = f"{BASE_URL}/train"
    response = requests.post(url, json=sample_model_data)

    # Assert response status code
    assert response.status_code == 200

    # Assert response content if necessary
    result = response.json()
    assert 'message' in result
    assert result['message'] == 'Model training successful'

def test_get_all_models(setup):
    # Simulate /models endpoint
    url = f"{BASE_URL}/models"
    response = requests.get(url)

    # Assert response status code
    assert response.status_code == 200

    # Assert response content if necessary
    models = response.json()
    assert isinstance(models, list)
    assert len(models) > 0
    assert all('model_name' in model for model in models)

def test_get_model_details(setup):
    # Simulate /models/{model_name} endpoint
    model_name = "LogisticRegression"
    url = f"{BASE_URL}/models/{model_name}"
    response = requests.get(url)

    # Assert response status code
    assert response.status_code == 200

    # Assert response content if necessary
    model_details = response.json()
    assert 'model_name' in model_details
    assert model_details['model_name'] == model_name
    assert 'model_params' in model_details

if __name__ == "__main__":
    pytest.main()
