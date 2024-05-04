from abc import ABC, abstractmethod

import pandas as pd

class DataPreprocessorBase(ABC):

    @abstractmethod
    def preprocess_dataset(self, dataset: pd.DataFrame, features_to_standardize: list[str]):
        pass
