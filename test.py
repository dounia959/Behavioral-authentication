import joblib

from src.dataset import build_dataset
from src.ensemble import predict_ensemble


scaler = joblib.load("models/scaler.pkl")
svm = joblib.load("models/svm.pkl")
iso = joblib.load("models/iso.pkl")

file_path = "data/test_session.csv"
X_test = build_dataset(file_path)

if len(X_test) == 0:
    raise Exception("No valid windows in test data")

final = predict_ensemble(svm, iso, scaler, X_test)

total = len(final)
legit = final.count(1)
anomaly = final.count(-1)

print(f"Total windows: {total}")
print(f"Legit: {legit}")
print(f"Anomaly: {anomaly}")

ratio = legit / total

if ratio > 0.9 :
    print("User is LEGIT")
else:
    print("Anomaly detected")
