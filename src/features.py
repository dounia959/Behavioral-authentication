import numpy as np


FEATURE_NAMES = [
    "dwell_mean",
    "dwell_std",
    "flight_mean",
    "flight_std",
    "typing_speed",
    "mouse_speed_mean",
    "mouse_speed_std",
    "mouse_acceleration_mean",
    "click_count",
    "pause_mean",
    "pause_max",
]


def extract_features(window):
    features = {}

    key_press = window[window["event_type"] == "key_press"]
    key_release = window[window["event_type"] == "key_release"]

    dwell = []
    for i in range(min(len(key_press), len(key_release))):
        dt = key_release.iloc[i]["timestamp"] - key_press.iloc[i]["timestamp"]
        if dt > 0:
            dwell.append(dt)

    features["dwell_mean"] = np.mean(dwell) if dwell else 0
    features["dwell_std"] = np.std(dwell) if dwell else 0

    press_times = key_press["timestamp"].to_numpy()
    if len(press_times) > 1:
        flight = np.diff(press_times)
        duration = press_times[-1] - press_times[0]
        features["flight_mean"] = np.mean(flight)
        features["flight_std"] = np.std(flight)
        features["typing_speed"] = len(press_times) / duration if duration > 0 else 0
    else:
        features["flight_mean"] = 0
        features["flight_std"] = 0
        features["typing_speed"] = 0

    mouse = window[window["event_type"] == "mouse_move"].dropna(subset=["x", "y"])
    if len(mouse) > 1:
        mouse_x = mouse["x"].astype(float).to_numpy()
        mouse_y = mouse["y"].astype(float).to_numpy()
        mouse_t = mouse["timestamp"].astype(float).to_numpy()

        dx = np.diff(mouse_x)
        dy = np.diff(mouse_y)
        dt = np.diff(mouse_t)
        valid_dt = np.where(dt > 0, dt, np.nan)

        speed = np.sqrt(dx**2 + dy**2) / valid_dt
        speed = speed[np.isfinite(speed)]

        features["mouse_speed_mean"] = np.mean(speed) if len(speed) else 0
        features["mouse_speed_std"] = np.std(speed) if len(speed) else 0

        if len(speed) > 1:
            acceleration = np.diff(speed)
            acceleration = acceleration[np.isfinite(acceleration)]
            features["mouse_acceleration_mean"] = np.mean(np.abs(acceleration)) if len(acceleration) else 0
        else:
            features["mouse_acceleration_mean"] = 0
    else:
        features["mouse_speed_mean"] = 0
        features["mouse_speed_std"] = 0
        features["mouse_acceleration_mean"] = 0

    clicks = window[window["event_type"] == "mouse_click"]
    features["click_count"] = len(clicks)

    event_times = window["timestamp"].astype(float).sort_values().to_numpy()
    pauses = np.diff(event_times)
    pauses = pauses[pauses > 0]
    features["pause_mean"] = np.mean(pauses) if len(pauses) else 0
    features["pause_max"] = np.max(pauses) if len(pauses) else 0

    return [float(features[name]) for name in FEATURE_NAMES]
