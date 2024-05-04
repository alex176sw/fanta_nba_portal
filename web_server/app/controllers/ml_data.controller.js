const NbaMatch = require('../models/nba_match');
const Mongo = require('./mongo');

class MLDataController {

    static async getTrainingData(req, res) {
        try {
            if (! Mongo.isMongoConnectionEstrablished()) {
                throw new Error('MongoDB connection is not established. Connection parameters: '+Mongo.getMongoConnectionConfig());
            }
    
            const ml_training_data = await NbaMatch.find();

            res.json(ml_training_data);

        }
        catch (error) {
            console.error('Error fetching data:', error);
            res.status(500).json({
                "error": error.toString()
            });
        }
    }
    
    static async getInferenceData(req, res) {
        const ml_inference_data = {
            "home_team": "Lakers",
            "away_team": "Chigago Bulls"
        }
        res.json(ml_inference_data);
    }
}

module.exports = MLDataController;