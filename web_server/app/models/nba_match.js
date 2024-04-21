const mongoose = require('mongoose');

const nbaMatchSchema = new mongoose.Schema({
    home_team: String,
    away_team: String
});

const NbaMatch = mongoose.model('NbaMatch', nbaMatchSchema);

module.exports = NbaMatch;
