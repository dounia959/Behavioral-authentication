# Continuous User Authentication using Behavioral Biometrics

## 📌 Overview

This project implements a continuous authentication system that verifies whether the current user of a computer is the legitimate owner based on behavioral patterns such as keystroke dynamics and mouse movements.

The system uses anomaly detection models (One-Class SVM and Isolation Forest) trained on user interaction data.

---

## 🧠 Key Idea

Instead of passwords, the system analyzes **how the user behaves**:

* typing rhythm
* mouse movement patterns
* interaction timing

---

## ⚙️ Pipeline

1. **Data Collection**

   * Keyboard and mouse events recorded using `pynput`
   * Each event includes timestamp, type, and position

2. **Windowing**

   * Data split into time windows (e.g., 10 seconds)
   * Also split on inactivity gaps

3. **Feature Extraction**

   * Dwell time (key hold duration)
   * Flight time (time between keys)
   * Typing speed
   * Mouse speed & acceleration
   * Click frequency
   * Pause behavior

4. **Dataset Creation**

   * Each window becomes a feature vector

5. **Model Training**

   * One-Class SVM (RBF kernel)
   * Isolation Forest

6. **Ensemble Decision**

   * Combine model outputs for final prediction

---

## 📊 Models Used

### One-Class SVM

* Learns boundary of normal behavior
* Kernel: RBF

### Isolation Forest

* Detects anomalies based on isolation

---

## 📈 Features Used

* dwell_mean, dwell_std
* flight_mean, flight_std
* typing_speed
* mouse_speed_mean, mouse_speed_std
* mouse_acceleration
* click_count
* pause_mean, pause_max

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Collect data

```bash
python src/collector.py
```

### 3. Build dataset

```bash
python src/dataset.py
```

### 4. Train models

```bash
python src/models.py
```

---

## 📂 Data

⚠️ Raw behavioral data is not included for privacy reasons.

---

## 🎯 Results

* Demonstrates feasibility of behavioral authentication
* Shows effectiveness of anomaly detection models
* Ensemble improves robustness

---

## ⚠️ Limitations

* User behavior varies over time
* Not foolproof against imitation
* Requires sufficient data collection

---

## 🔮 Future Work

* Add deep learning models (LSTM, Autoencoder)
* Improve feature engineering (digraphs, rhythm)
* Implement real-time authentication system

---

## 👨‍💻 Author

LILIA MOKHTARI

---

