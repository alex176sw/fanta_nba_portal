var express = require('express');
const userDataRouter = require('./routes/user_data.router');
const UserDataController = require('./controllers/user_data.controller');


var app = express();
app.get('/', function (req, res) {
    res.send('FANTA NBA SERVICE');
});

app.use('/get_training_data', userDataRouter);

// Handle other endpoints or invalid requests
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// port is configurable
const port = process.env.PORT;

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