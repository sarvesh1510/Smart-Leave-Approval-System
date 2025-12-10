# ai_model/train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib, os

#  Load dataset
data_path = os.path.join(os.path.dirname(__file__), "leave_history.csv")
data = pd.read_csv(data_path)
print(f" Loaded CSV successfully from: {data_path}")

#  Encode categorical columns
label_encoders = {}
for col in ['department', 'role', 'leave_type', 'approval_status']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

#  Define features and target
X = data[['department', 'role', 'leave_type', 'leave_duration', 'previous_leaves', 'team_on_leave_ratio']]
y = data['approval_status']

#  Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#  Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#  Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f" Model trained successfully with accuracy: {accuracy * 100:.2f}%")

#  Save both model and encoders
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
encoder_path = os.path.join(os.path.dirname(__file__), "encoders.pkl")

joblib.dump(model, model_path)
joblib.dump(label_encoders, encoder_path)

print(f" Model saved at: {model_path}")
print(f" Encoders saved at: {encoder_path}")
