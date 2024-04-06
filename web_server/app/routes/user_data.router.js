const express = require('express');
const router = express.Router();
const UserDataController = require('../controllers/user_data.controller');

// Handle the /users endpoint
router.get('/', UserDataController.getData);

// Add more routes for the /users endpoint as needed

module.exports = router;