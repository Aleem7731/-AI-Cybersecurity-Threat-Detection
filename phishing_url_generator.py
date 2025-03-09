import pandas as pd
import random

phishing_urls = [
    "http://paypal-security-update.com",
    "http://bank-verification-alert.com",
    "http://free-gift-cards.net",
    "http://win-free-money.com",
] * 2500  # Create 10,000 phishing samples

safe_urls = [
    "https://www.paypal.com",
    "https://www.bankofamerica.com",
    "https://www.amazon.com",
    "https://www.netflix.com",
] * 2500  # Create 10,000 safe samples

data = [(url, 1) for url in phishing_urls] + [(url, 0) for url in safe_urls]
random.shuffle(data)

df = pd.DataFrame(data, columns=["url", "label"])
df.to_csv("useful_csv\phishing_url_dataset.csv", index=False)
print("Dataset saved as phishing_url_dataset.csv")
