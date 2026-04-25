import numpy as np

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

    press_times = key_press["timestamp"].values
    if len(press_times) > 1:
        flight = np.diff(press_times)
        features["flight_mean"] = np.mean(flight)
        features["flight_std"] = np.std(flight)
        features["typing_speed"] = len(press_times) / (press_times[-1] - press_times[0])
    else:
        features["flight_mean"] = 0
        features["flight_std"] = 0
        features["typing_speed"] = 0

    mouse = window[window["event_type"] == "mouse_move"]
    if len(mouse) > 1:
        dx = np.diff(mouse["x"])
        dy = np.diff(mouse["y"])
        dt = np.diff(mouse["timestamp"])
        speed = np.sqrt(dx**2 + dy**2) / (dt + 1e-5)

        features["mouse_speed_mean"] = np.mean(speed)
        features["mouse_speed_std"] = np.std(speed)
    else:
        features["mouse_speed_mean"] = 0
        features["mouse_speed_std"] = 0

    clicks = window[window["event_type"] == "mouse_click"]
    features["click_count"] = len(clicks)

    return list(features.values())