const mongoose = require('mongoose');
const config = require('config');

const nbaMatchSchema = new mongoose.Schema({
    home_team: String,
    away_team: String
});

const NbaMatch = mongoose.model(config.db.document, nbaMatchSchema);

module.exports = NbaMatch;
