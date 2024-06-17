const config = require('config');

class MLDataController {
    static async getOverviewData(req, res) {
        const fetchModule = await import('node-fetch');
        const fetch = fetchModule.default;        
        const mlManagerConfig = config.get('ml_manager_service');
        const fetch_url = `http://${mlManagerConfig.host}:${mlManagerConfig.port}/overview`;
        console.log("getOverviewData:",fetch_url)

        try {
            const response = await fetch(fetch_url);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const overviewData = await response.json();
            res.json(overviewData);
        } catch (error) {
            console.error("Error fetching overview data:", error);
            res.status(500).json({ "error": error.message });
        }
    }

    static async trainModel(req, res) {
        const fetchModule = await import('node-fetch');
        const fetch = fetchModule.default;        
        const mlManagerConfig = config.get('ml_manager_service');
        const fetch_url = `http://${mlManagerConfig.host}:${mlManagerConfig.port}/train`;
        console.log("trainModel:",fetch_url)

        try {
            const response = await fetch(fetch_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(req.body)
            });
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }
            const trainData = await response.json();
            res.json(trainData);
        } catch (error) {
            console.error("Error training model:", error);
            res.status(500).json({ "error": error.message });
        }
    }

    static async makeInference(req, res) {
        const fetchModule = await import('node-fetch');
        const fetch = fetchModule.default;        
        const mlManagerConfig = config.get('ml_manager_service');

        const { homeTeam, hostTeam, trainedModel } = req.body;
        const fetch_url = `http://${mlManagerConfig.host}:${mlManagerConfig.port}/inference` + '?homeTeam=' + encodeURIComponent(homeTeam) + '&hostTeam=' + encodeURIComponent(hostTeam)+ '&trainedModel='+ encodeURIComponent(trainedModel);
        console.log("makeInference:",fetch_url)
        try {
            const response = await fetch(fetch_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(req.body)
            });
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }
            const inferenceData = await response.json();
            res.json(inferenceData);
        } catch (error) {
            console.error("Error making inference:", error);
            res.status(500).json({ "error": error.message });
        }
    }
}

module.exports = MLDataController;
