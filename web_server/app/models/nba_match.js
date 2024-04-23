const mongoose = require('mongoose');

const nbaMatchSchema = new mongoose.Schema({
    home_team: String,
    away_team: String
});

const NbaMatch = mongoose.model('match', nbaMatchSchema);

module.exports = NbaMatch;
