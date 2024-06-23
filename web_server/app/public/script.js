document.addEventListener('DOMContentLoaded', () => {
    fetchOverviewData();
});


function fetchOverviewData() {
    fetch('/ml/overview')
        .then(response => {
            if (!response.ok) {
                return response.text().then(errorText => {
                    throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            displayOverviewData(data);
        })
        .catch(error => displayError(error.message));
}


function displayOverviewData(data) {
    // Display trained models
    const trainedModelsList = document.getElementById('trainedModelsList');
    trainedModelsList.innerHTML = '';
    data.trainedModels.forEach(model => {
        const li = document.createElement('li');
        li.textContent = model.model_type + " - " + formatUnixTimestamp(model.timestamp) + " (Params: C=" + model.model_params.C + ", Intercept="+model.model_params.intercept_scaling+")";
        trainedModelsList.appendChild(li);
    });

    // Display queue length
    document.getElementById('queueLength').innerHTML = `<strong>Train queue length: </strong> <span>${data.trainQueueLength}</span><br><strong>Inference queue length: </strong> <span>${data.inferenceQueueLength}</span>`;


    // Display training results
    const tableBody = document.getElementById('trainingResultsTable').querySelector('tbody');
    tableBody.innerHTML = '';

    data.trainingResults.forEach(result => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${formatUnixTimestamp(result.timestamp)}</td>
            <td>${result._id}</td>
            <td>${result.model_type}</td>
            <td>${result.message}</td>
        `;
        tableBody.appendChild(row);

    });

    // Display inference results
    const tableBodyI = document.getElementById('inferenceResultsTable').querySelector('tbody');
    tableBodyI.innerHTML = '';
    data.inferenceResults.forEach(result => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${formatUnixTimestamp(result.timestamp)}</td>
            <td>${result.home_team_win_prob}</td>
            <td>${result.host_team_win_prob}</td>
            <td>${result.message}</td>
        `;
        tableBodyI.appendChild(row);
    });

    // Populate trained models dropdown for inference
    const trainedModelSelect = document.getElementById('trainedModel');
    trainedModelSelect.innerHTML = '';
    data.trainedModels.forEach(model => {
        const option = document.createElement('option');
        option.textContent = model.model_type+ " " + formatUnixTimestamp(model.timestamp) + " " + model._id;
        option.value = model._id;
        trainedModelSelect.appendChild(option);
    });
}

function trainModel() {
    const modelType = document.getElementById('modelType').value;
    fetch('/ml/train', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ modelType })
    })
    .then(response => {
        console.log(response);
        if (!response.ok) {
            return response.text().then(errorText => {
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            });
        }
        return response.json();
    })
    .then(data => {
        displayTrainOutput(data);
    })
    .catch(error => displayError(error.message));

}

function displayTrainOutput(data) {
    const output = document.getElementById('train-output');
    output.innerHTML = `<strong>Success! </strong> <span>${data.message}</span>`;
    output.className = 'alert alert-success'; 
}

function makeInference() {
    const homeTeam = document.getElementById('homeTeam').value;
    const hostTeam = document.getElementById('hostTeam').value;
    const trainedModel = document.getElementById('trainedModel').value;
    console.log("makeInference: ", trainedModel)
    fetch('/ml/inference', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ homeTeam, hostTeam, trainedModel })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(errorText => {
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            });
        }
        return response.json();
    })
    .then(data => {
        displayInferenceOutput(data);
    })
    .catch(error => displayError(error.message));
}

function displayInferenceOutput(data) {
    const output = document.getElementById('inference-output');
    output.innerHTML = `<strong>Success! </strong> <span>${data.message}</span>`;
    output.className = 'alert alert-success'; // Add the Bootstrap classes for alert success
}

function displayError(errorMessage) {
    const errorContainer = document.getElementById('error-container');
    errorContainer.innerHTML = `<strong>Error:</strong> <span>${errorMessage}</span>`;
    errorContainer.style.color = 'red';
    errorContainer.style.fontWeight = 'bold';    
}

function formatUnixTimestamp(timestamp) {
    let date = new Date(timestamp * 1000);
    
    let formattedDate = `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
    
    return formattedDate;
}
