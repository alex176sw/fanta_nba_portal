var express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const MLDataRouter = require('./routes/ml_data.router');

var app = express();

app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());


app.get('/', function (req, res) {
    res.sendFile(__dirname + '/public/index.html');
});

app.use('/get_ml_data', MLDataRouter);

// Handle other endpoints or invalid requests
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/fantanba')
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Could not connect to MongoDB', err));

// port is configurable
const port = process.env.PORT | 3000;

app.listen(port, function () {
    console.log('Example app listening on port '+port);
});



/*
Deployment and Scaling:
Prepare your API for deployment by configuring environment variables and setting up necessary infrastructure.
– Store sensitive information like database credentials in environment variables.
– Use a configuration library like dotenv to load environment variables.
Deploy your Node.js API to a cloud platform like AWS, Google Cloud, or Heroku.
– Follow the platform-specific deployment instructions for your chosen cloud provider.
Implement scaling strategies such as load balancing and horizontal scaling to handle increased traffic.
– Utilize containerization technologies like Docker and container orchestration tools like Kubernetes to manage scalability efficiently.
*/