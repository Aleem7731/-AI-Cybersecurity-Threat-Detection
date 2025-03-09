import streamlit as st
import requests

# Set Streamlit page configuration
st.set_page_config(page_title="Phishing Detection Dashboard", layout="wide")

# Define API base URL
API_URL = "http://127.0.0.1:5000"

# Theme Toggle
st.sidebar.markdown('<h3 style="text-align:center; color:#FF5733;">🌗 Select Theme:</h3>', unsafe_allow_html=True)
theme = st.sidebar.radio("", ["🌞 Light Mode", "🌙 Dark Mode"])

# Apply custom CSS based on theme
if theme == "🌙 Dark Mode":
    theme_css = """
    <style>
        body {background-color: #121212; color: gold;}
        .title {background: linear-gradient(to right, #ff416c, #ff4b2b); color: gold;}
        [data-testid="stSidebar"] {background-color: #222; color: gold;}
        div.stButton > button {background-color: #444; color: gold;}
        div.stButton > button:hover {background-color: #ff4b2b; color: gold;}
        .success {color: lightgreen; font-weight: bold;}
        .error {color: red; font-weight: bold;}
        .footer {color: white; text-align: center;}
        .theme-text {color: #FFD700; font-weight: bold; text-align: center;}
        .lock-icon {color: gold; text-align: center; font-size: 50px;}
        div[role="radiogroup"] label div {color: gold !important;}
    </style>
    """
    theme_text = '<h4 class="theme-text">Dark Mode Activated 🌙</h4>'
else:
    theme_css = """
    <style>
        body {background-color: #f5f5f5; color: black;}
        .title {background: linear-gradient(to right, #0062ff, #00c6ff); color: white;}
        [data-testid="stSidebar"] {background-color: #f0f0f0; color: black;}
        div.stButton > button {background-color: #007bff; color: white;}
        div.stButton > button:hover {background-color: #0056b3; color: white;}
        .success {color: green; font-weight: bold;}
        .error {color: red; font-weight: bold;}
        .footer {color: black; text-align: center;}
        .theme-text {color: #FF5733; font-weight: bold; text-align: center;}
        div[role="radiogroup"] label div {color: black !important;}
    </style>
    """
    theme_text = '<h4 class="theme-text">Light Mode Activated 🌞</h4>'

st.markdown(theme_css, unsafe_allow_html=True)
st.sidebar.markdown(theme_text, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title" style="text-align:center;padding:15px;border-radius:10px;">🔍 AI-Powered Phishing Detection System</h1>', unsafe_allow_html=True)

# Sidebar Information
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/565/565547.png", width=100)
st.sidebar.markdown("### 🔹 Features:")
st.sidebar.markdown("✔️ AI-based Phishing Detection")
st.sidebar.markdown("✔️ Email & URL Analysis")
st.sidebar.markdown("✔️ Real-time Results")
st.sidebar.markdown("✔️ Detailed Explanations")
st.sidebar.markdown("---")

# Tabs for Email & URL detection
tab1, tab2 = st.tabs(["📧 Email Phishing Detection", "🔗 URL Phishing Detection"])

with tab1:
    st.subheader("📩 Check if an Email is Phishing")
    email_text = st.text_area("Paste the email content here:")
    
    if st.button("Analyze Email"):
        if email_text.strip():
            try:
                response = requests.post(f"{API_URL}/predict/email", json={"email_text": email_text})
                if response.status_code == 200:
                    result = response.json()
                    prediction = result['prediction']
                    
                    if prediction == "Safe":
                        st.success(f"✅ Prediction: {prediction}", icon="✅")
                    else:
                        st.error(f"❌ Prediction: {prediction}", icon="🚨")
                    
                    st.info("📌 **Why this prediction?**\n\n- If Phishing: Email contains suspicious links, urgent requests, or misleading content.\n- If Safe: No phishing patterns detected.")
                else:
                    st.error(f"❌ API Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Failed: {e}")
        else:
            st.warning("⚠️ Please enter email content before analyzing.")

with tab2:
    st.subheader("🔗 Check if a URL is Phishing")
    url_text = st.text_input("Enter the URL to analyze:")
    
    if st.button("Analyze URL"):
        if url_text.strip():
            try:
                response = requests.post(f"{API_URL}/predict/url", json={"url": url_text})
                if response.status_code == 200:
                    result = response.json()
                    prediction = result['prediction']
                    
                    if prediction == "Safe":
                        st.success(f"✅ Prediction: {prediction}", icon="✅")
                    else:
                        st.error(f"❌ Prediction: {prediction}", icon="🚨")
                    
                    st.info("📌 **Why this prediction?**\n\n- If Phishing: URL is linked to malicious domains, suspicious patterns, or known attack vectors.\n- If Safe: No malicious characteristics found.")
                else:
                    st.error(f"❌ API Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Failed: {e}")
        else:
            st.warning("⚠️ Please enter a URL before analyzing.")

# Footer with developer names & guide credit at the bottom
st.sidebar.markdown(
    """
    <div class="footer">
        👨‍💻 **Developed by:**<br>
        💡 Shaik Aleem<br>
        💡 K. Daksha Daya<br>
        💡 G. Sai Lakshman<br><br>
        🏆 **Guided by:**<br>
        🎓 MD. Abdul Aziz
    </div>
    """,
    unsafe_allow_html=True
)