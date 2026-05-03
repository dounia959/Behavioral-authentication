import numpy as np
import pandas as pd

from src.features import FEATURE_NAMES, extract_features
from src.windowing import create_windows


REQUIRED_COLUMNS = {"timestamp", "event_type", "key", "x", "y"}


def build_dataset(file_path):
    df = pd.read_csv(file_path, encoding="latin1")
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_cols}")

    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df["x"] = pd.to_numeric(df["x"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df = df.dropna(subset=["timestamp", "event_type"])

    if df.empty:
        return np.empty((0, len(FEATURE_NAMES)))

    windows = create_windows(df)

    X = []
    for window in windows:
        if len(window) > 20:
            X.append(extract_features(window))

    if not X:
        return np.empty((0, len(FEATURE_NAMES)))

    return np.array(X, dtype=float)
