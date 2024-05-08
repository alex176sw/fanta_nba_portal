//const NbaMatch = require('../models/nba_match');
//const Mongo = require('./mongo');
const config = require('config');
class MLDataController {

    static async getTrainingData(req, res) {
        const fetchModule = await import('node-fetch');
        const fetch = fetchModule.default;
        const mlConfig = config.get('ml_data_service');

        const fetch_url = "http://" + mlConfig.host + ':' + mlConfig.port + '/' + mlConfig.get_training_data_end_point;
        console.log("Fetching url: "+fetch_url)

        try {
            const response = await fetch(fetch_url);
            const ml_inference_data = await response.json();
            res.json(ml_inference_data);
        } catch (error) {
            console.log("error!", error);
            res.status(500).json({"error": error.message});
        }
    }
    

    static async getInferenceData(req, res) {
        const fetchModule = await import('node-fetch');
        const fetch = fetchModule.default;
        const mlConfig = config.get('ml_data_service');


        const { homeTeam, awayTeam } = req.body;
        const fetch_url = "http://" + mlConfig.host + ':' + mlConfig.port + '/' + mlConfig.get_inference_data_end_point + '?homeTeam=' + encodeURIComponent(homeTeam) + '&awayTeam=' + encodeURIComponent(awayTeam);

        console.log("Fetching url: "+fetch_url)
        
        try {
            const response = await fetch(fetch_url);
            const ml_inference_data = await response.json();
            console.log("ml_inference_data:",ml_inference_data)
            res.json(ml_inference_data);
        } catch (error) {
            console.log("error!", error);
            res.status(500).json({"error": error.message});
        }
    }
    
    


}

module.exports = MLDataController;