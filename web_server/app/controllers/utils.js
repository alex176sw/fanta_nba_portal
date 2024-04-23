const mongoose = require('mongoose');

class Utils {
    static isMongoConnectionEstrablished(data) {
        return mongoose.connection.readyState == 1        
    }

}

module.exports = Utils;
