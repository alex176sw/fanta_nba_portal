class DataPreprocessing {
    static preprocessData(data) {
        return data.map(match => ({
            home_team: match.home_team.toUpperCase(),
            away_team: match.away_team.toLowerCase()
        }));
    }
}

module.exports = DataPreprocessing;
