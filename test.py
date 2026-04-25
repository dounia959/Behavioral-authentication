import joblib
from src.dataset import build_dataset

# Load models
scaler = joblib.load("models/scaler.pkl")
svm = joblib.load("models/svm.pkl")
iso = joblib.load("models/iso.pkl")

# Load test data
file_path = "data/test_session.csv"
X_test = build_dataset(file_path)

if len(X_test) == 0:
    raise Exception("No valid windows in test data")

X_scaled = scaler.transform(X_test)

# Predictions
svm_pred = svm.predict(X_scaled)
iso_pred = iso.predict(X_scaled)

# Ensemble decision
final = []
for s, i in zip(svm_pred, iso_pred):
    if s == 1 and i == 1:
        final.append(1)
    else:
        final.append(-1)

# Results
total = len(final)
legit = final.count(1)
anomaly = final.count(-1)

print(f"Total windows: {total}")
print(f"Legit: {legit}")
print(f"Anomaly: {anomaly}")

# Final decision
ratio = legit / total

if ratio > 0.7:
    print("✅ User is LEGIT")
else:
    print("⚠️ Anomaly detected")