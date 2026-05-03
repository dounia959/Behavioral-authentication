# Continuous User Authentication using Behavioral Biometrics

## Overview

This project implements a continuous authentication prototype that checks whether the current computer user looks like the legitimate owner based on behavioral patterns such as keystroke timing and mouse movement.

The system trains anomaly detection models on normal user activity and flags later sessions that do not match the learned pattern.

## Pipeline

1. Data collection
   - Keyboard and mouse events are recorded with `pynput`.
   - Each event includes timestamp, event type, key, and mouse position.

2. Windowing
   - Raw events are split into 10-second windows.
   - Long inactivity gaps start a new segment.

3. Feature extraction
   - Dwell time
   - Flight time
   - Typing speed
   - Mouse speed
   - Mouse acceleration
   - Click count
   - Pause statistics

4. Model training
   - One-Class SVM
   - Isolation Forest

5. Ensemble prediction
   - A window is accepted only when both models classify it as normal.

## Setup

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

On systems where `python` is configured normally, this also works:

```bash
python -m pip install -r requirements.txt
```

## Usage

Collect a new behavioral session:

```bash
py src/collector.py
```

Train models from `data/data_record.csv`:

```bash
py main.py
```

Evaluate `data/test_session.csv` with the saved models:

```bash
py test.py
```

## Expected CSV Format

Input files must contain these columns:

```text
timestamp,event_type,key,x,y
```

Supported event types include:

```text
key_press
key_release
mouse_move
mouse_click
mouse_scroll
```

## Notes

Raw behavioral data can be sensitive. Keep collected sessions private and avoid committing personal datasets unless they are sanitized.
