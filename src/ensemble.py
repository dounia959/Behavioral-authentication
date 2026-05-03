def predict_ensemble(svm, iso, scaler, X):
    if len(X) == 0:
        return []

    X_scaled = scaler.transform(X)
    svm_pred = svm.predict(X_scaled)
    iso_pred = iso.predict(X_scaled)

    final = []
    for s, i in zip(svm_pred, iso_pred):
        if s == 1 and i == 1:
            final.append(1)
        else:
            final.append(-1)

    return final
