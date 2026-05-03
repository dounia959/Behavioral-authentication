def create_windows(df, window_size=10, gap_threshold=5):
    if df.empty:
        return []

    df = df.sort_values("timestamp").reset_index(drop=True)
    gap_id = (df["timestamp"].diff().fillna(0) > gap_threshold).cumsum()
    segment_start = df.groupby(gap_id)["timestamp"].transform("first")
    elapsed = df["timestamp"] - segment_start
    fixed_window_id = (elapsed // window_size).astype(int)

    grouped = df.groupby([gap_id, fixed_window_id], sort=False)
    return [window for _, window in grouped]
