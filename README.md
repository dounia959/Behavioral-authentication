# Continuous User Authentication using Behavioral Biometrics

## Overview

This project implements a **continuous authentication system** based on **behavioral biometrics**.  
Instead of relying only on passwords, the system continuously verifies user identity using behavioral patterns such as:

-  Keystroke dynamics
-  Mouse movement behavior
-  Typing rhythm
-  Interaction speed and pauses

The project uses **machine learning anomaly detection models** trained on legitimate user behavior to detect suspicious or abnormal sessions in real time.

The system includes:

-  Complete behavioral data collection pipeline
-  Machine learning training and testing
-  Flask backend API
-  Modern web interface
   Real-time logs and authentication results

---

# 🎥 Demo Video

> https://youtu.be/2jaQqqaOu7U


#  Features

##  Authentication Features

- Continuous user authentication
- Behavioral biometric analysis
- Real-time anomaly detection
- Ensemble prediction system
- Session-based verification

---

##  Behavioral Features Extracted

- Dwell time
- Flight time
- Typing speed
- Mouse speed
- Mouse acceleration
- Click count
- Pause statistics

---

##  Machine Learning Models

- One-Class SVM
- Isolation Forest
- Ensemble decision mechanism

---

## Web Application Features

- Upload behavioral CSV files
- Real-time behavioral data collection
- Train models directly from the browser
- Authentication testing interface
- Real-time training logs
- Result visualization
- Reset system functionality
- Responsive UI

---

# Project Architecture

## Data Collection

Keyboard and mouse events are recorded using `pynput`.

Captured information includes:

- Timestamp
- Event type
- Pressed key
- Mouse coordinates
- Mouse clicks and scrolls

---

##  Windowing

Raw events are divided into:

- 10-second behavioral windows
- New segments created after inactivity periods

---

##  Feature Extraction

Behavioral features are extracted from each window and transformed into machine-learning-ready vectors.

---

##  Model Training

The system trains unsupervised anomaly detection models using legitimate user behavior only.

---

##  Authentication

Incoming behavioral sessions are analyzed and classified as:

- ✅ LEGITIMATE USER
- ❌ ANOMALOUS USER

---

#  Technologies Used

## Backend

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- pynput

---

## Frontend

- HTML
- CSS
- JavaScript

---

## Machine Learning

- One-Class SVM
- Isolation Forest

---

# Project Structure

```bash
project/
│
├── app.py
├── main.py
├── test.py
├── requirements.txt
│
├── src/
│   ├── collector.py
│   ├── feature_extraction.py
│   ├── training.py
│   └── ...
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
├── data/
│   ├── data_record.csv
│   └── test_session.csv
│
├── models/
│
└── docs/
```

---

#  Installation

## 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

---

## 2️⃣ Install Dependencies

```bash
py -m pip install -r requirements.txt
```

or

```bash
python -m pip install -r requirements.txt
```

---

# Running the Project

## 1️⃣ Start the Flask Server

Run:

```bash
python app.py
```

The server will start at:

```txt
http://localhost:5000
```

---

## 2️⃣ Open the Web Interface

Open your browser and go to:

```txt
http://localhost:5000
```

---

## 3️⃣ Collect Behavioral Data

You have two options:

###  Option A : Real-Time Collection

Open another terminal and run:

```bash
python src/collector.py
```

Then:

- Type normally
- Move the mouse naturally
- Continue for 30–60 seconds
- Press `ESC` to stop

The generated CSV file can then be uploaded through the web interface.

---

###  Option B : Upload Existing CSV

Upload an already collected behavioral dataset directly from the web interface.

---

## 4️⃣ Train the Models

Inside the web interface:

- Click **"Start Training"**
- Watch real-time logs
- Wait for:

```txt
 Training complete!
```

The system will train:

- One-Class SVM
- Isolation Forest

and save the generated models.

---

## 5️⃣ Run Authentication Testing

### Steps

1. Collect a new behavioral session
2. Upload the test CSV
3. Click:

```txt
Run Authentication Test
```

---

### Results

The system will display:

-  LEGIT
-  ANOMALY
-  Confidence score
-  Authentication statistics

---

#  Command-Line Usage

##  Collect Data

```bash
python src/collector.py
```

---

##  Train Models

```bash
python main.py
```

---

##  Test Authentication

```bash
python test.py
```

---

#  Expected CSV Format

Input CSV files must contain:

```csv
timestamp,event_type,key,x,y
```

Supported event types:

```txt
key_press
key_release
mouse_move
mouse_click
mouse_scroll
```

---

#  API & Backend Capabilities

The Flask backend provides:

- File upload endpoints
- Model training endpoints
- Authentication testing endpoints
- System reset endpoints
- Real-time log streaming

The architecture is modular and extensible for future behavioral modalities.

---

#  Testing Scenarios

##  Scenario 1 : Legitimate User

1. Collect normal behavioral data
2. Train the system
3. Test using similar behavior

Expected result:

```txt
LEGIT ✓
```

---

## 🚨 Scenario 2 : Impostor Detection

1. Train using one user's behavior
2. Test using significantly different behavior

Expected result:

```txt
ANOMALY ✗
```

---

## ⚠️ Scenario 3 — Edge Cases

### Minimal Data

Expected:

- Helpful validation error

### Invalid CSV Format

Expected:

- Format validation error

### Reset System

Expected:

- Models deleted
- Fresh retraining possible

---

#  Key Capabilities

##  For End Users

- No command-line interaction required
- Easy-to-use graphical interface
- Clear authentication results
- Real-time progress visualization

---

##  For Developers

- Modular architecture
- Extensible API
- Well-structured backend
- Easy feature integration

---

## For Researchers

- Configurable parameters
- Observable ML workflow
- Access to logs and metrics
- Reproducible experiments

---

# 🔒 Security & Privacy Notes

Behavioral biometric data is sensitive.

## Recommendations

- Do not publish raw user behavioral datasets
- Store only extracted features when possible
- Protect trained behavioral models
- Obtain user consent before data collection

---

#  Future Improvements

Possible future extensions:

- Touchscreen gesture support
- Deep learning models
- Real-time continuous monitoring
- Adaptive model retraining
- Multi-user support

---


```

