import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM

from src.utils import ensure_dirs


MAX_SVM_SAMPLES = 100000


def train_models(X):
    if len(X) == 0:
        raise ValueError("Cannot train models with an empty dataset.")

    ensure_dirs()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    if len(X_scaled) > MAX_SVM_SAMPLES:
        X_svm = X_scaled[:MAX_SVM_SAMPLES]
    else:
        X_svm = X_scaled

    svm = OneClassSVM(kernel="rbf", nu=0.1, gamma="scale")
    svm.fit(X_svm)

    iso = IsolationForest(contamination=0.1, random_state=42)
    iso.fit(X_scaled)

    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(svm, "models/svm.pkl")
    joblib.dump(iso, "models/iso.pkl")

    return svm, iso
