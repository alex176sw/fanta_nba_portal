const express = require('express');
const router = express.Router();
const MLDataController = require('../controllers/ml_data.controller');

router.get('/overview', MLDataController.getOverviewData);
router.post('/train', MLDataController.trainModel);
router.post('/inference', MLDataController.makeInference);

module.exports = router;
