import pytest
import argparse
from trainer.trainer import TrainerService
from sklearn.utils.validation import check_is_fitted

def test_train_model():
    args = argparse.Namespace()
    args.mongo_config_file = "trainer/config/default.yaml"
    trainer = TrainerService(args)


    model_type = "logistic-regression"
    data = {
        "records": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    }
    model = trainer.train_model(model_type, data)
    check_is_fitted(model)

    with pytest.raises(Exception):
        model_type = "logistic-regression"
        data = {
            "records": []
        }
        model = trainer.train_model(model_type, data)

