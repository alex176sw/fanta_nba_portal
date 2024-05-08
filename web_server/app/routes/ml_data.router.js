const express = require('express');
const router = express.Router();
const MLDataController = require('../controllers/ml_data.controller');

router.get('/train', MLDataController.getTrainingData);
router.post('/inference', MLDataController.getInferenceData);


module.exports = router;