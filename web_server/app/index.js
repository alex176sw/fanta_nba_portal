var express = require('express');
//const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const MLDataRouter = require('./routes/ml_data.router');
//const Mongo = require('./controllers/mongo');

var app = express();

app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/public/index.html');
});

app.use('/ml', MLDataRouter);

// Handle other endpoints or invalid requests
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// port is configurable
const port = process.env.PORT | 3000;

app.listen(port, function () {
    console.log('Example app listening on port '+port);
});