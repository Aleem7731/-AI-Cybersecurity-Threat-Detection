import os
import pandas as pd
import joblib
import scipy.sparse
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

#######################################
#  TRAIN PHISHING EMAIL MODEL         #
#######################################

# Load phishing email dataset
email_df = pd.read_csv("useful_csv/phishing_email_cleaned.csv")

# Rename column if necessary: use "text_combined" as email text
if "text_combined" in email_df.columns:
    email_df.rename(columns={"text_combined": "email_text"}, inplace=True)
elif "email_text" not in email_df.columns:
    raise ValueError("❌ Email dataset must have 'text_combined' or 'email_text' column.")

# Ensure label column exists
if "label" not in email_df.columns:
    raise ValueError("❌ Email dataset must have 'label' column.")

# Fill missing values
email_df["email_text"] = email_df["email_text"].fillna("")
email_df["label"] = pd.to_numeric(email_df["label"], errors="coerce").fillna(0).astype(int)

print("📊 Email dataset label distribution before SMOTE:")
print(email_df["label"].value_counts())

# Vectorize email text
email_vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_email = email_vectorizer.fit_transform(email_df["email_text"])
y_email = email_df["label"]

# Convert to dense for SMOTE
X_email_dense = X_email.toarray()
if len(set(y_email)) > 1:
    smote_email = SMOTE(random_state=42)
    X_email_resampled, y_email_resampled = smote_email.fit_resample(X_email_dense, y_email)
    print("✅ SMOTE applied for emails.")
else:
    print("⚠️ Only one class found in email dataset, skipping SMOTE.")
    X_email_resampled, y_email_resampled = X_email_dense, y_email

# Split email dataset
X_email_train, X_email_test, y_email_train, y_email_test = train_test_split(
    X_email_resampled, y_email_resampled, test_size=0.2, random_state=42
)

# Train email model
email_model = RandomForestClassifier(n_estimators=100, random_state=42)
email_model.fit(X_email_train, y_email_train)

# Save email model and vectorizer
joblib.dump(email_model, "models/phishing_email_model.pkl")
joblib.dump(email_vectorizer, "models/email_vectorizer.pkl")
print("✅ Email model and vectorizer trained and saved.")

#######################################
#  TRAIN PHISHING URL MODEL           #
#######################################

# Load phishing URL dataset
url_df = pd.read_csv("useful_csv/phishing_url_dataset.csv")

# Ensure required columns exist
if "url" not in url_df.columns or "label" not in url_df.columns:
    raise ValueError("❌ URL dataset must have 'url' and 'label' columns.")

# Fill missing values
url_df["url"] = url_df["url"].fillna("")
url_df["label"] = pd.to_numeric(url_df["label"], errors="coerce").fillna(0).astype(int)

print("📊 URL dataset label distribution before SMOTE:")
print(url_df["label"].value_counts())

# Vectorize URL text
url_vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")
X_url = url_vectorizer.fit_transform(url_df["url"])
y_url = url_df["label"]

# Convert to dense for SMOTE
X_url_dense = X_url.toarray()
if len(set(y_url)) > 1:
    smote_url = SMOTE(random_state=42)
    X_url_resampled, y_url_resampled = smote_url.fit_resample(X_url_dense, y_url)
    print("✅ SMOTE applied for URLs.")
else:
    print("⚠️ Only one class found in URL dataset, skipping SMOTE.")
    X_url_resampled, y_url_resampled = X_url_dense, y_url

# Split URL dataset
X_url_train, X_url_test, y_url_train, y_url_test = train_test_split(
    X_url_resampled, y_url_resampled, test_size=0.2, random_state=42
)

# Train URL model
url_model = RandomForestClassifier(n_estimators=100, random_state=42)
url_model.fit(X_url_train, y_url_train)

# Save URL model and vectorizer
joblib.dump(url_model, "models/phishing_url_model.pkl")
joblib.dump(url_vectorizer, "models/url_vectorizer.pkl")
print("✅ URL model and vectorizer trained and saved!")
