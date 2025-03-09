import pickle
import re
from urllib.parse import urlparse

# Function to load pickle files safely
def load_pickle(file_path):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

# Load models and vectorizers
email_model = load_pickle("models/phishing_email_model.pkl")
url_model = load_pickle("models/phishing_url_model.pkl")
email_vectorizer = load_pickle("models/tfidf_vectorizer.pkl")
url_vectorizer = load_pickle("models/url_vectorizer.pkl")

def check_url(url):
    """Check if a URL is phishing or not"""
    if not url_model or not url_vectorizer:
        return "Error: Model or vectorizer not loaded."
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Basic feature extraction
    url_length = len(url)
    num_dots = url.count(".")
    num_slashes = url.count("/")

    # Combine into feature vector
    url_features = [f"{domain} {path} {url_length} {num_dots} {num_slashes}"]
    url_vectorized = url_vectorizer.transform(url_features)

    # Predict
    prediction = url_model.predict(url_vectorized)[0]
    return "Phishing" if prediction == 1 else "Legitimate"

def check_email(email_text):
    """Check if an email is phishing or not"""
    if not email_model or not email_vectorizer:
        return "Error: Model or vectorizer not loaded."
    
    email_vectorized = email_vectorizer.transform([email_text])

    # Predict
    prediction = email_model.predict(email_vectorized)[0]
    return "Phishing" if prediction == 1 else "Legitimate"

if __name__ == "__main__":
    choice = input("Check (1) URL or (2) Email? Enter 1 or 2: ")

    if choice == "1":
        test_url = input("Enter a URL to check: ")
        print(check_url(test_url))
    elif choice == "2":
        test_email = input("Enter email text to check: ")
        print(check_email(test_email))
    else:
        print("Invalid choice! Please enter 1 or 2.")
