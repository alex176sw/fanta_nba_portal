function getTrainingData() {
    fetch('/get_ml_data/train')
        .then(response => response.json())
        .then(data => displayData(data))
        .catch(error => displayError(error));
}

function getInferenceData() {
    const homeTeam = document.getElementById('homeTeam').value;
    const awayTeam = document.getElementById('awayTeam').value;
    fetch('/get_ml_data/inference', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ homeTeam, awayTeam })
    })
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
