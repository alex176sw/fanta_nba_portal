function getTrainingData() {
    fetch('/get_ml_data/train')
        .then(response => response.json())
        .then(data => {
            if (data.columns && data.records && data.target) {
                data.records = data.records.map((record, index) => {
                    record[0] = data.target[index];
                    return record;
                });
            }        
            displayData(data)
            console.log(data)
        })
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
    const output = document.getElementById('output');
    output.innerHTML = '';  // Clear previous content

    if (data.columns && data.records) {
        const table = document.createElement('table');
        table.classList.add('table', 'table-striped');

        // Create table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        data.columns.forEach(column => {
            const th = document.createElement('th');
            th.textContent = column;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Create table body
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
        output.textContent = 'No data available';
    }
}

function displayError(error) {
    document.getElementById('output').textContent = error.toString();
}
