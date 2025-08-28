import pandas as pd
import joblib

# Load trained model & scaler
model = joblib.load("models/fraud_rf.pkl")
scaler = joblib.load("models/scaler.pkl")

def predict_transaction(transaction):
    """
    transaction = dict with keys:
    ['Time', 'V1', 'V2', ..., 'V28', 'Amount']
    """
    # Convert to DataFrame
    df = pd.DataFrame([transaction])

    # Scale 'Time' and 'Amount'
    df[['Time', 'Amount']] = scaler.transform(df[['Time', 'Amount']])

    # Predict
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return prediction, probability

if __name__ == "__main__":
    # Example test transaction
    test_transaction = {
        "Time": 100000,
        "V1": -1.5, "V2": 0.7, "V3": -0.2, "V4": 1.1,
        "V5": -0.3, "V6": 0.9, "V7": -1.2, "V8": 0.5,
        "V9": -0.8, "V10": 0.2, "V11": 1.3, "V12": -0.5,
        "V13": 0.4, "V14": -0.6, "V15": 1.0, "V16": -1.4,
        "V17": 0.6, "V18": -0.7, "V19": 0.3, "V20": -0.9,
        "V21": 0.8, "V22": -0.2, "V23": 0.7, "V24": -1.1,
        "V25": 0.9, "V26": -0.4, "V27": 1.2, "V28": -0.3,
        "Amount": 150
    }

    pred, prob = predict_transaction(test_transaction)
    print(f"Prediction: {'Fraud' if pred == 1 else 'Not Fraud'}")
    print(f"Fraud Probability: {prob:.4f}")