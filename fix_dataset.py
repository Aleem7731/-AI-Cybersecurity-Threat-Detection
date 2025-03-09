import pandas as pd
import scipy.sparse
import joblib
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load phishing email dataset
email_df = pd.read_csv("useful_csv/phishing_email_cleaned.csv")
url_df = pd.read_csv("useful_csv/phishing_url_dataset.csv")

# Rename columns to match expected format
email_df.rename(columns={"text_combined": "email_text"}, inplace=True)

# Ensure both datasets have the correct columns
if "email_text" not in email_df.columns or "label" not in email_df.columns:
    raise ValueError("❌ Email dataset must have 'email_text' and 'label' columns.")

if "url" not in url_df.columns or "label" not in url_df.columns:
    raise ValueError("❌ URL dataset must have 'url' and 'label' columns.")

# Fill missing values
email_df["email_text"] = email_df["email_text"].fillna("")
email_df["url"] = ""  # Add empty 'url' column to match structure

url_df["url"] = url_df["url"].fillna("")
url_df["email_text"] = ""  # Add empty 'email_text' column to match structure

# Merge both datasets
df = pd.concat([email_df, url_df], ignore_index=True)

# Print label distribution before balancing
print("📊 Label Distribution Before SMOTE:")
print(df["label"].value_counts())

# Initialize TF-IDF Vectorizers
email_vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
url_vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")

# Fit & transform email_text and URL separately
X_text = email_vectorizer.fit_transform(df["email_text"])
X_url = url_vectorizer.fit_transform(df["url"])

# Combine email & URL features
X_combined = scipy.sparse.hstack((X_text, X_url))

# Labels
y = df["label"]

# Convert sparse matrix to dense format for SMOTE
X_combined_dense = X_combined.toarray()

# Apply SMOTE only if more than 1 class exists
if len(set(y)) > 1:
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_combined_dense, y)
    print("✅ SMOTE applied successfully.")
else:
    print("⚠️ No phishing samples found! Skipping SMOTE.")
    X_resampled, y_resampled = X_combined_dense, y

# Convert back to DataFrame
df_resampled = pd.DataFrame(X_resampled)
df_resampled["label"] = y_resampled

# Save the balanced dataset
df_resampled.to_csv("useful_csv\balanced_dataset.csv", index=False)
print("✅ SMOTE-balanced dataset saved as 'balanced_dataset.csv'")

# Print label distribution after SMOTE
print("📊 Label Distribution After SMOTE:")
print(pd.Series(y_resampled).value_counts())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save models and vectorizers
joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(email_vectorizer, "models/email_vectorizer.pkl")
joblib.dump(url_vectorizer, "models/url_vectorizer.pkl")

print("✅ Models trained and saved successfully!")    
