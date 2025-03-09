import joblib
from scipy.sparse import hstack

# Load the trained phishing detection model and vectorizers
email_model = joblib.load("models/phishing_model.pkl")
email_vectorizer = joblib.load("models/email_vectorizer.pkl")
url_vectorizer = joblib.load("models/url_vectorizer.pkl")

# Sample test input
test_email = ["Your PayPal account has been limited. Click here to restore access."]
test_url = ["http://secure-paypal.com"]

# Transform input using the same vectorizers from training
email_features = email_vectorizer.transform(test_email)
url_features = url_vectorizer.transform(test_url)

# Merge email and URL features
input_features = hstack([email_features, url_features])

# Predict phishing or not
email_prediction = email_model.predict(input_features)  # Ensure input is vectorized
print(f"Prediction: {'Phishing' if email_prediction[0] == 1 else 'Safe'}")
