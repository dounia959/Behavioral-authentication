import pandas as pd

def create_windows(df, window_size=10, gap_threshold=5):
    df = df.sort_values("timestamp").reset_index(drop=True)

    windows = []
    current = []

    start_time = df.loc[0, "timestamp"]
    last_time = start_time

    for _, row in df.iterrows():
        t = row["timestamp"]

        if t - last_time > gap_threshold:
            if current:
                windows.append(pd.DataFrame(current))
                current = []
            start_time = t

        elif t - start_time > window_size:
            windows.append(pd.DataFrame(current))
            current = []
            start_time = t

        current.append(row)
        last_time = t

    if current:
        windows.append(pd.DataFrame(current))

    return windows