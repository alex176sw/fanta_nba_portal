const mongoose = require('mongoose');
const config = require('config');


class Mongo {
    static connect() {
        const dbConfig = config.get('db');        
        mongoose.connect('mongodb://'+dbConfig.host+':'+dbConfig.port+'/'+dbConfig.collection)
            .then(() => console.log('Connected to MongoDB. Collection: '+dbConfig.collection))
            .catch(err => console.error('Could not connect to MongoDB', err));
    }
    static isMongoConnectionEstrablished() {
        return mongoose.connection.readyState == 1        
    }

}

module.exports = Mongo;
