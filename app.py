import streamlit as st
import pickle
import numpy as np
import os

# -----------------------------------
# Load Models (Robust Path Handling)
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'models/model_hr.pkl'), 'rb') as f:
    model_hr = pickle.load(f)

with open(os.path.join(BASE_DIR, 'models/model_bt.pkl'), 'rb') as f:
    model_bt = pickle.load(f)

with open(os.path.join(BASE_DIR, 'models/model_cal.pkl'), 'rb') as f:
    model_cal = pickle.load(f)

# -------------------------------
# Helper Functions
# -------------------------------
def prepare_inputs(user_input, model_hr, model_bt):
    if user_input['Heart_Rate'] is None:
        features = np.array([[user_input['Gender'], user_input['Age'], user_input['Height'], user_input['Weight'], user_input['Duration']]])
        user_input['Heart_Rate'] = model_hr.predict(features)[0]

    if user_input['Body_Temp'] is None:
        features = np.array([[user_input['Gender'], user_input['Age'], user_input['Height'], user_input['Weight'], user_input['Duration']]])
        user_input['Body_Temp'] = model_bt.predict(features)[0]

    return user_input

def predict_calories(user_input, model_cal):
    features = np.array([[user_input['Gender'], user_input['Age'], user_input['Height'],
                          user_input['Weight'], user_input['Duration'],
                          user_input['Heart_Rate'], user_input['Body_Temp']]])
    return round(model_cal.predict(features)[0], 1)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🔥 SmartBurn - Calorie Burn Predictor")
st.markdown("Estimate how many calories you burn based on your personal metrics and workout session.")

# Collect inputs
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=10, max_value=100)
height = st.number_input("Height (cm)", min_value=100, max_value=250)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
duration = st.number_input("Workout Duration (mins)", min_value=1, max_value=300)

# Optional fields
heart_rate = st.number_input("Heart Rate (optional)", min_value=50, max_value=200, step=1, format="%d", value=None)
body_temp = st.number_input("Body Temperature (optional)", min_value=35.0, max_value=40.0, step=0.1, format="%.1f", value=None)

# Prediction
if st.button("🔥 Predict Calories Burned"):
    user_input = {
        'Gender': 1 if gender == "Male" else 0,
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Duration': duration,
        'Heart_Rate': heart_rate if heart_rate else None,
        'Body_Temp': body_temp if body_temp else None
    }

    # Predict missing inputs and calories
    user_input = prepare_inputs(user_input, model_hr, model_bt)
    predicted_calories = predict_calories(user_input, model_cal)

    # Output
    st.success(f"Estimated Calories Burned: {predicted_calories} kcal")
    st.info(f"Heart Rate used: {user_input['Heart_Rate']:.1f} bpm")
    st.info(f"Body Temperature used: {user_input['Body_Temp']:.1f} °C")
