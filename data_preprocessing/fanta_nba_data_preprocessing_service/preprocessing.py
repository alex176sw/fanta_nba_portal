import pandas as pd
from sklearn.preprocessing import StandardScaler

def standardize(dataset):
    dataset = pd.DataFrame(dataset)
    columns = list(dataset.columns)

    scaler = StandardScaler()

    dataset = scaler.fit_transform(dataset).tolist()

    return dataset, columns, scaler.mean_.tolist(), scaler.scale_.tolist()
        