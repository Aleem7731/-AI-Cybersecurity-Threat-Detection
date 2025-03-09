import joblib
import os
from urllib.parse import urlparse

# Define model and vectorizer paths
email_model_path = "models/phishing_email_model.pkl"
email_vectorizer_path = "models/email_vectorizer.pkl"
url_model_path = "models/phishing_url_model.pkl"
url_vectorizer_path = "models/url_vectorizer.pkl"

# Load models and vectorizers with error handling
def load_model(path, name):
    """Loads a model or vectorizer with error handling."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ {name} file not found: {path}")
        return joblib.load(path)
    except Exception as e:
        print(f"❌ Error loading {name}: {e}")
        return None

# Load phishing email and URL models
email_model = load_model(email_model_path, "Email Model")
email_vectorizer = load_model(email_vectorizer_path, "Email Vectorizer")
url_model = load_model(url_model_path, "URL Model")
url_vectorizer = load_model(url_vectorizer_path, "URL Vectorizer")

def check_email(email_text):
    """Check if an email is phishing or legitimate."""
    if not email_model or not email_vectorizer:
        return "❌ Email model not loaded. Please check errors."

    email_text = email_text.strip()
    if not email_text:
        return "⚠️ Please enter valid email text."

    email_vectorized = email_vectorizer.transform([email_text])
    prediction = email_model.predict(email_vectorized)[0]
    return "🔴 Phishing Email" if prediction == 1 else "🟢 Legitimate Email"

def check_url(url):
    """Check if a URL is phishing or legitimate."""
    if not url_model or not url_vectorizer:
        return "❌ URL model not loaded. Please check errors."

    url = url.strip()
    if not url:
        return "⚠️ Please enter a valid URL."

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Basic URL feature extraction
    url_length = len(url)
    num_dots = url.count(".")
    num_slashes = url.count("/")

    # Combine into feature vector
    url_features = [f"{domain} {path} {url_length} {num_dots} {num_slashes}"]
    url_vectorized = url_vectorizer.transform(url_features)

    # Predict
    prediction = url_model.predict(url_vectorized)[0]
    return "🔴 Phishing URL" if prediction == 1 else "🟢 Legitimate URL"

if __name__ == "__main__":
    print("🚀 Phishing Detection System (Emails & URLs)")

    while True:
        choice = input("\nCheck (1) Email or (2) URL? Enter 1, 2, or 'exit' to quit: ").strip().lower()
        
        if choice == "exit":
            print("👋 Exiting program.")
            break
        elif choice == "1":
            email = input("📩 Enter email text: ").strip()
            print(check_email(email))
        elif choice == "2":
            url = input("🔗 Enter URL: ").strip()
            print(check_url(url))
        else:
            print("⚠️ Invalid choice! Please enter 1, 2, or 'exit'.")
