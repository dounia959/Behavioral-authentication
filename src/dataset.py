import pandas as pd
import numpy as np
from src.windowing import create_windows
from src.features import extract_features

def build_dataset(file_path):
    df = pd.read_csv(file_path)
    windows = create_windows(df)

    X = []
    for w in windows:
        if len(w) > 20:
            X.append(extract_features(w))

    return np.array(X)