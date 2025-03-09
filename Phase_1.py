import streamlit as st
import joblib
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load pre-trained model and vectorizer
try:
    vectorizer = joblib.load("models/vectorizer.pkl")  
    model = joblib.load("models/phishing_model.pkl")  
except FileNotFoundError as e:
    st.error(f"Error: {e}. Please ensure the model files exist in the 'models' folder.")
    st.stop()

# Function to preprocess email text
def preprocess_email(email_text):
    email_text = email_text.lower()
    email_text = re.sub(r'http\S+', ' URL ', email_text)  # Replace links with 'URL'
    email_text = re.sub(r'[^a-zA-Z\s]', '', email_text)  # Remove special characters
    email_text = re.sub(r'\s+', ' ', email_text).strip()  # Remove extra spaces
    return email_text

# Function to classify email using AI
def detect_phishing(email_text):
    processed_text = preprocess_email(email_text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)[0]
    return "⚠️ Phishing Detected!" if prediction == 1 else "✅ Safe Email."

# Streamlit UI
st.set_page_config(page_title="AI Phishing Detection", page_icon="📧", layout="centered")

st.title("📧 AI Phishing Email Detection")
st.markdown("Enter the email content below to check if it's a phishing email.")

email_input = st.text_area("Paste Email Content Here", height=200)

if st.button("Scan Email"):
    if email_input.strip():
        result = detect_phishing(email_input)
        st.success(result)
    else:
        st.warning("⚠️ Please enter email content.")
