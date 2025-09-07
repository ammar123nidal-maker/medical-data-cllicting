# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state dataframe
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "name", "age", "gender", "hight", "wieght",
        "sys BP", "Dia BP", "heart rate",
        "HbA1c", "Cholesterol", "HDL", "LDL", "Triglycerides",
        "degree of improvement"
    ])

st.title("🧑‍⚕️ Patient Data Collection and Analysis")

st.sidebar.header("➕ Add New Patient")

# Input form
with st.sidebar.form("patient_form"):
    name = st.text_input("Patient Name")
    gender = st.selectbox("Gender", ["male", "female"])
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    hight = st.number_input("Height (cm)", min_value=0.0)
    weight = st.number_input("Weight (kg)", min_value=0.0)

    st.subheader("Vitals")
    sys_bp = st.number_input("Systolic BP", min_value=0)
    dia_bp = st.number_input("Diastolic BP", min_value=0)
    heart_rate = st.number_input("Heart Rate", min_value=0)

    st.subheader("Lab Results")
    hba1c = st.number_input("HbA1c", min_value=0.0, format="%.2f")
    cholesterol = st.number_input("Cholesterol", min_value=0.0)
    hdl = st.number_input("HDL", min_value=0.0)
    ldl = st.number_input("LDL", min_value=0.0)
    triglycerides = st.number_input("Triglycerides", min_value=0.0)

    degree = st.selectbox("Degree of Improvement", ["High", "Moderate", "Low"])

    submitted = st.form_submit_button("Add Patient")

    if submitted:
        new_patient = pd.DataFrame([{
            "name": name, "age": age, "gender": gender,
            "hight": hight, "wieght": weight,
            "sys BP": sys_bp, "Dia BP": dia_bp, "heart rate": heart_rate,
            "HbA1c": hba1c, "Cholesterol": cholesterol,
            "HDL": hdl, "LDL": ldl, "Triglycerides": triglycerides,
            "degree of improvement": degree
        }])
        st.session_state.df = pd.concat([st.session_state.df, new_patient], ignore_index=True)
        st.success(f"✅ Patient {name} added successfully!")

st.subheader("📋 Patients Data")
st.dataframe(st.session_state.df)

if not st.session_state.df.empty:
    st.subheader("📊 Data Analysis")

    st.write("**Summary Statistics**")
    st.write(st.session_state.df.describe().round(2))

    st.write("**Filter Patients by Name**")
    filter_name = st.text_input("Enter patient name to filter")
    if filter_name:
        st.dataframe(st.session_state.df[st.session_state.df["name"] == filter_name])

    st.write("**Patients with HbA1c > 5.7**")
    st.dataframe(st.session_state.df[st.session_state.df["HbA1c"] > 5.7])

    st.subheader("📈 Visualization")

    # Gender distribution
    gender_counts = st.session_state.df['gender'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
    ax1.set_title("Distribution of Gender")
    st.pyplot(fig1)

    # Degree of improvement bar chart
    fig2, ax2 = plt.subplots()
    st.session_state.df["degree of improvement"].value_counts().plot(
        kind="bar", ax=ax2, color=["green", "orange", "red"]
    )
    ax2.set_title("Degree of Improvement")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

    # Save data
    st.download_button(
        label="💾 Download Data as CSV",
        data=st.session_state.df.to_csv(index=False).encode("utf-8"),
        file_name="patients_data.csv",
        mime="text/csv",
    )
