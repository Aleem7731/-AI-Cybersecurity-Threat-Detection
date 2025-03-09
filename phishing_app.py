from flask import Flask, request, jsonify
import joblib
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Define model and vectorizer paths
models = {
    "email_model": "models/phishing_email_model.pkl",
    "email_vectorizer": "models/email_vectorizer.pkl",
    "url_model": "models/phishing_url_model.pkl",
    "url_vectorizer": "models/url_vectorizer.pkl"
}

# Load models and vectorizers
def load_model(path, name):
    """Loads a model or vectorizer with error handling."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ {name} file not found: {path}")
        return joblib.load(path)
    except Exception as e:
        print(f"❌ Error loading {name}: {e}")
        return None

email_model = load_model(models["email_model"], "Email Model")
email_vectorizer = load_model(models["email_vectorizer"], "Email Vectorizer")
url_model = load_model(models["url_model"], "URL Model")
url_vectorizer = load_model(models["url_vectorizer"], "URL Vectorizer")

@app.route("/")
def home():
    return jsonify({"status": "✅ Phishing Detection API is running!"})

@app.route("/predict/email", methods=["POST"])
def predict_email():
    if email_model is None or email_vectorizer is None:
        return jsonify({"error": "❌ Email phishing model or vectorizer is missing"}), 500

    data = request.json
    email_text = data.get("email_text", "").strip()

    if not email_text:
        return jsonify({"error": "⚠️ No email text provided"}), 400

    email_features = email_vectorizer.transform([email_text])
    prediction = email_model.predict(email_features)[0]
    result = "Phishing" if prediction == 1 else "Safe"

    return jsonify({"email_text": email_text, "prediction": result})

@app.route("/predict/url", methods=["POST"])
def predict_url():
    if url_model is None or url_vectorizer is None:
        return jsonify({"error": "❌ URL phishing model or vectorizer is missing"}), 500

    data = request.json
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "⚠️ No URL provided"}), 400

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Extract basic URL features
    url_length = len(url)
    num_dots = url.count(".")
    num_slashes = url.count("/")

    # Combine into feature vector
    url_features = [f"{domain} {path} {url_length} {num_dots} {num_slashes}"]
    url_vectorized = url_vectorizer.transform(url_features)

    # Predict
    prediction = url_model.predict(url_vectorized)[0]
    result = "Phishing" if prediction == 1 else "Safe"

    return jsonify({"url": url, "prediction": result})

if __name__ == "__main__":
    print("🚀 Starting Flask server on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
