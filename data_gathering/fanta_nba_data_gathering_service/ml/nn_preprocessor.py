from data_gathering.ml.data_preprocessor_base import DataPreprocessorBase

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


class NNPreProcessor(DataPreprocessorBase):

    def preprocess_dataset(self, dataset: pd.DataFrame, features_to_standardize: list[str]) -> np.ndarray:
        
        dataset.dropna(inplace=True)

        scaler = StandardScaler()

        dataset[features_to_standardize] = scaler.fit_transform(dataset[features_to_standardize])

        return dataset
