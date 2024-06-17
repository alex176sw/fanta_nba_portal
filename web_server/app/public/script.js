document.addEventListener('DOMContentLoaded', () => {
    fetchOverviewData();
});


function fetchOverviewData() {
    fetch('/ml/overview')
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
            displayOverviewData(data);
        })
        .catch(error => displayError(error.message));
}


function displayOverviewData(data) {
    // Display trained models
    console.log(data);
    const trainedModelsList = document.getElementById('trainedModelsList');
    trainedModelsList.innerHTML = '';
    data.trainedModels.forEach(model => {
        const li = document.createElement('li');
        li.textContent = model.model_type + " (Params:" + model.model_params + ")";
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
            <td>${result.timestamp}</td>
            <td>${result.model_type}</td>
            <td>${result.message}</td>
        `;
        tableBody.appendChild(row);
    });


    // Display inference results
    tableBody = document.getElementById('inferenceResultsTable').querySelector('tbody');
    tableBody.innerHTML = '';
    data.inferenceResults.forEach(result => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${result.timestamp}</td>
            <td>${result.homeTeamWinningPercentage}</td>
            <td>${result.hostTeamWinningPercentage}</td>
            <td>${result.message}</td>
        `;
        tableBody.appendChild(row);
    });

    // Populate trained models dropdown for inference
    const trainedModelSelect = document.getElementById('trainedModel');
    trainedModelSelect.innerHTML = '';
    data.trainedModels.forEach(model => {
        const option = document.createElement('option');
        option.value = model.model_type;
        option.textContent = model.model_type;
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
    fetch('/ml/inference', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ homeTeam, hostTeam, trainedModel })
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
        displayInferenceOutput(data);
    })
    .catch(error => displayError(error.message));
}

function displayInferenceOutput(data) {
    const output = document.getElementById('inference-output');
    output.innerHTML = `<strong>Success! </strong> <span>${data.message}</span>`;
    output.className = 'alert alert-success'; // Add the Bootstrap classes for alert success
}


function displayData(data) {
    const output = document.getElementById('output');
    output.innerHTML = '';  // Clear previous content

    if (data.columns && data.records) {
        const table = document.createElement('table');
        table.classList.add('table', 'table-striped');

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        data.columns.forEach(column => {
            const th = document.createElement('th');
            th.textContent = column;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        data.records.forEach(record => {
            const row = document.createElement('tr');
            record.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
        table.appendChild(tbody);

        output.appendChild(table);
    } else {
        output.textContent = "No data available";
    }
}

function displayError(errorMessage) {
    const errorContainer = document.getElementById('error-container');
    errorContainer.innerHTML = `<strong>Error:</strong> <span>${errorMessage}</span>`;
    errorContainer.style.color = 'red';
    errorContainer.style.fontWeight = 'bold';    
}