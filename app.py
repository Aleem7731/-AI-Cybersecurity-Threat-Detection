import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

# Streamlit Configuration
st.set_page_config(page_title="Phishing Detection", layout="wide")

# Session State for User Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- LOGIN PAGE ---
def login_page():
    st.title("🔐 Login to Your Account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.session_state.username = response.json()["username"]
            st.success("✅ Login Successful!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid Username or Password")

# --- SIGNUP PAGE ---
def signup_page():
    st.title("📝 Create a New Account")
    username = st.text_input("Choose a Username", key="signup_user")
    password = st.text_input("Choose a Password", type="password", key="signup_pass")

    if st.button("Sign Up"):
        response = requests.post(f"{API_URL}/signup", json={"username": username, "password": password})
        if response.status_code == 201:
            st.success("✅ Account Created Successfully! Please Login.")
        else:
            st.error("❌ Username already exists.")

# --- DASHBOARD ---
def dashboard():
    st.sidebar.markdown(f"**👤 Welcome, {st.session_state.username}!**")
    st.sidebar.button("Logout", on_click=lambda: logout())

    tab1, tab2 = st.tabs(["📧 Email Phishing Detection", "🔗 URL Phishing Detection"])
    
    with tab1:
        st.subheader("📩 Email Phishing Detection")
        email_text = st.text_area("Paste the email content here:")
        if st.button("Analyze Email"):
            if email_text:
                response = requests.post(f"{API_URL}/predict/email", json={"email_text": email_text})
                prediction = response.json().get("prediction", "Error")
                if prediction == "Safe":
                    st.success(f"✅ Prediction: {prediction}")
                else:
                    st.error(f"🚨 Prediction: {prediction}")
            else:
                st.warning("⚠️ Please enter email content.")

    with tab2:
        st.subheader("🔗 URL Phishing Detection")
        url_text = st.text_input("Enter the URL:")
        if st.button("Analyze URL"):
            if url_text:
                response = requests.post(f"{API_URL}/predict/url", json={"url": url_text})
                prediction = response.json().get("prediction", "Error")
                if prediction == "Safe":
                    st.success(f"✅ Prediction: {prediction}")
                else:
                    st.error(f"🚨 Prediction: {prediction}")
            else:
                st.warning("⚠️ Please enter a URL.")

# --- LOGOUT FUNCTION ---
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()

# --- PAGE NAVIGATION ---
page = st.sidebar.radio("Navigation", ["Login", "Sign Up", "Dashboard"])

if page == "Login":
    login_page()
elif page == "Sign Up":
    signup_page()
elif page == "Dashboard":
    if st.session_state.logged_in:
        dashboard()
    else:
        st.warning("⚠️ Please Login First")
        login_page() 

