import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Features (X) and Target (y)
X = df.drop("Class", axis=1)
y = df["Class"]

# Standardize 'Amount' & 'Time'
scaler = StandardScaler()
X[['Time', 'Amount']] = scaler.fit_transform(X[['Time', 'Amount']])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Handle imbalance with SMOTE
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("Original dataset shape:", y.value_counts().to_dict())
print("Resampled dataset shape:", y_train_resampled.value_counts().to_dict())

# Train RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train_resampled, y_train_resampled)

# Quick accuracy check
test_accuracy = model.score(X_test, y_test)
print(f"✅ Test Accuracy: {test_accuracy:.4f}")

# Save model + scaler
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fraud_rf.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("✅ Model and scaler saved in 'models/' folder")
