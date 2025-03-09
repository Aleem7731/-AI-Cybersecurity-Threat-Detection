import pandas as pd
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset (replace 'dataset.csv' with your actual file)
df = pd.read_csv("dataset.csv")

# Rename columns if needed
df.columns = ["url", "label"]  # Ensure columns are ['url', 'label']
df["label"] = df["label"].map({"phishing": 1, "safe": 0})  # Convert labels

# Preprocessing function
def preprocess_url(url):
    url = url.lower()
    url = re.sub(r"https?://", "", url)  # Remove http/https
    url = re.sub(r"www.", "", url)  # Remove 'www'
    url = re.sub(r"\W+", " ", url)  # Remove special characters
    return url

df["clean_url"] = df["url"].apply(preprocess_url)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(df["clean_url"], df["label"], test_size=0.2, random_state=42)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

# Save vectorizer & model
joblib.dump(vectorizer, "models/vectorizer.pkl")
joblib.dump(model, "models/phishing_model.pkl")

# Test accuracy
y_pred = model.predict(X_test_tfidf)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")
