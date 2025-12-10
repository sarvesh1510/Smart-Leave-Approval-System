import os
import joblib
import pandas as pd

# Auto-load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(MODEL_PATH)

def predict_leave_approval(department, role, leave_type, leave_duration, previous_leaves, team_on_leave_ratio):
    """Predict if a leave request should be approved or rejected using trained AI model."""
    # Encode categorical data manually (same logic used during training)
    label_maps = {
        'department': {'IT': 0, 'HR': 1, 'Finance': 2, 'Marketing': 3, 'Operations': 4},
        'role': {'Employee': 0, 'Manager': 1, 'Admin': 2},
        'leave_type': {'Sick': 0, 'Casual': 1, 'Vacation': 2}
    }

    # Default fallback if unseen
    dept_val = label_maps['department'].get(department, 0)
    role_val = label_maps['role'].get(role, 0)
    leave_type_val = label_maps['leave_type'].get(leave_type, 0)

    # Prepare dataframe for prediction
    features = pd.DataFrame([{
        "department": dept_val,
        "role": role_val,
        "leave_type": leave_type_val,
        "leave_duration": leave_duration,
        "previous_leaves": previous_leaves,
        "team_on_leave_ratio": team_on_leave_ratio
    }])

    prediction = model.predict(features)[0]
    return "Approved" if prediction == 1 else "Rejected"
