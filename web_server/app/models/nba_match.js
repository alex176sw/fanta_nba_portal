const mongoose = require('mongoose');
const config = require('config');


const nbaMatchSchema = new mongoose.Schema({
    ml_training_set: []
});

const NbaMatch = mongoose.model(config.db.collection, nbaMatchSchema);

module.exports = NbaMatch;
