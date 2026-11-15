import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Concrete Strength Prediction",
    page_icon="🏗️",
    layout="wide"
)

# -----------------------------
# Load Model
# -----------------------------

@st.cache_resource
def load_model():
    return joblib.load("models/best_model.pkl")

bundle = load_model()

model = bundle["model"]
feature_names = bundle["feature_names"]
stats = bundle["feature_stats"]

# -----------------------------
# Application Title
# -----------------------------

st.title("🏗️ Concrete Compressive Strength Prediction")

st.write("""
This application predicts the compressive strength of concrete
based on its ingredients and age.
""")

st.divider()

# -----------------------------
# Sidebar User Inputs
# -----------------------------

st.sidebar.header("Concrete Mixture Parameters")

labels = [
    "Cement (kg/m³)",
    "Blast Furnace Slag (kg/m³)",
    "Fly Ash (kg/m³)",
    "Water (kg/m³)",
    "Superplasticizer (kg/m³)",
    "Coarse Aggregate (kg/m³)",
    "Fine Aggregate (kg/m³)",
    "Age (days)"
]

def user_input():

    data = {}

    for column, label in zip(feature_names, labels):

        minimum = float(stats["min"][column])
        maximum = float(stats["max"][column])
        mean = float(stats["mean"][column])

        if column == feature_names[-1]:
            value = st.sidebar.slider(
                label,
                min_value=int(minimum),
                max_value=int(maximum),
                value=int(mean),
                step=1
            )

        else:
            value = st.sidebar.slider(
                label,
                min_value=minimum,
                max_value=maximum,
                value=mean,
                step=0.1
            )

        data[column] = value

    features = pd.DataFrame([data], columns=feature_names)

    return features


# Get user inputs
input_df = user_input()

# -----------------------------
# Main Page
# -----------------------------

st.subheader("Selected Concrete Mixture")

st.dataframe(
    input_df,
    use_container_width=True
)

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Concrete Strength", type="primary"):

    prediction = model.predict(input_df)[0]

    st.success("Prediction completed successfully!")

    st.metric(
        label="Predicted Compressive Strength",
        value=f"{prediction:.2f} MPa"
    )

    st.write(
        "This is the estimated compressive strength "
        "for the selected concrete mixture."
    )

    st.info(
        "Note: This prediction is an estimate from a "
        "Machine Learning model, not a laboratory test."
    )
