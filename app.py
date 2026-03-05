import streamlit as st
import pandas as pd
import pickle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Calories Predictor", layout="wide")
st.title("🔥 Calories Burned Analysis & Prediction")

# --- Step 1: Automatic Data Loading ---
try:
    # This looks for the file directly in your folder
    df = pd.read_csv('calories_data.csv')
    
    st.success("✅ Dataset loaded successfully!")
    
    # --- Step 2 & 3: Understanding & Visualization ---
    st.write("### 📋 Data Preview (First 5 Rows)")
    st.dataframe(df.head())

    st.write("### 📊 Visualizing the Data")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Duration vs Calories**")
        fig1, ax1 = plt.subplots()
        sns.scatterplot(data=df, x='Duration', y='Calories_Burned', ax=ax1, color='crimson')
        st.pyplot(fig1)
    
    with col2:
        st.write("**Heart Rate Distribution**")
        fig2, ax2 = plt.subplots()
        sns.histplot(df['Heart_Rate'], kde=True, ax=ax2, color='royalblue')
        st.pyplot(fig2)

    # --- Step 8: Prediction UI ---
    st.divider()
    st.write("### 🤖 Predict Your Calories")
    
    # Load the pre-trained model
    try:
        model = pickle.load(open('model.pkl', 'rb'))
        
        c1, c2, c3 = st.columns(3)
        with c1:
            dur = st.number_input("Exercise Duration (mins)", value=20)
        with c2:
            hr = st.number_input("Average Heart Rate", value=100)
        with c3:
            temp = st.number_input("Body Temperature (Celsius)", value=37.0)

        if st.button("Calculate Burned Calories"):
            features = np.array([[dur, hr, temp]])
            prediction = model.predict(features)
            st.metric(label="Estimated Calories", value=f"{prediction[0]:.2f} kcal")
            
    except FileNotFoundError:
        st.error("Missing 'model.pkl'. Please run your Jupyter Notebook to generate the model file first!")

except FileNotFoundError:
    st.error("Missing 'calories_data.csv'. Please make sure the CSV file is in the same folder as this app.")