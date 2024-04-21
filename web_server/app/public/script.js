function getTrainingData() {
    fetch('/get_ml_data/train')
        .then(response => response.json())
        .then(data => displayData(data))
        .catch(error => displayError(error));
}

function getInferenceData() {
    fetch('/get_ml_data/inference')
        .then(response => response.json())
        .then(data => displayData(data))
        .catch(error => displayError(error));
}

function displayData(data) {
    document.getElementById('output').innerHTML = JSON.stringify(data);
}

function displayError(error) {
    document.getElementById('output').innerHTML = error.toString();
}
