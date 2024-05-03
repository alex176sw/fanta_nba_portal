const mongoose = require('mongoose');
const config = require('config');


class Mongo {
    static connect() {
        const dbConfig = config.get('db');
        const connection_string = 'mongodb://'+dbConfig.host+':'+dbConfig.port+'/'+dbConfig.database  
        mongoose.connect(connection_string)
            .then(() => console.log('Connected to MongoDB database: '+dbConfig.database))
            .catch(
                err => console.error('Could not connect to MongoDB with connection string: '+connection_string, err)
                
            );
    }
    static isMongoConnectionEstrablished() {
        return mongoose.connection.readyState == 1;
    }
    static getMongoConnectionConfig() {
        return JSON.stringify(config.get('db'));
    }

}

module.exports = Mongo;
