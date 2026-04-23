import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from preprocess import clean_text

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("data/tweets.csv")

# If synthetic data already has sentiment column → OK
# If not, we create simple labels

if "sentiment" not in df.columns:
    def simple_label(text):
        text = text.lower()
        if "love" in text or "great" in text or "amazing" in text:
            return "positive"
        elif "worst" in text or "hate" in text or "terrible" in text:
            return "negative"
        return "neutral"

    df["sentiment"] = df["text"].apply(simple_label)

# -----------------------------
# 2. CLEAN TEXT
# -----------------------------
df["clean"] = df["text"].apply(clean_text)

# -----------------------------
# 3. FEATURES
# -----------------------------
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["clean"])
y = df["sentiment"]

# -----------------------------
# 4. TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

# -----------------------------
# 5. TRAIN MODEL
# -----------------------------
model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)

# -----------------------------
# 6. EVALUATE
# -----------------------------
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print(f"\n✅ Model Accuracy: {acc:.2f}")

# -----------------------------
# 7. SAVE MODEL
# -----------------------------
joblib.dump(model, "models/model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("✅ Model and vectorizer saved!")