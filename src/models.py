from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

def train_models(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    svm = OneClassSVM(kernel='rbf', nu=0.1, gamma='scale')
    svm.fit(X_scaled)

    iso = IsolationForest(contamination=0.1)
    iso.fit(X_scaled)

    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(svm, "models/svm.pkl")
    joblib.dump(iso, "models/iso.pkl")

    return svm, iso