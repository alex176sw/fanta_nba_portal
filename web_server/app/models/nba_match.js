const mongoose = require('mongoose');
const config = require('config');


const nbaMatchSchema = new mongoose.Schema({
    games_stats: []
});

const NbaMatch = mongoose.model(config.db.collection, nbaMatchSchema);

module.exports = NbaMatch;
