import pandas as pd
from collections import Counter
import re

# -----------------------------
# STOPWORDS (simple)
# -----------------------------
STOPWORDS = {
    "the", "is", "a", "an", "and", "or", "to", "of", "in",
    "for", "on", "with", "this", "that", "it", "i", "you",
    "my", "we", "our"
}

# -----------------------------
# EMOTION KEYWORDS + EMOJIS
# -----------------------------
EMOTION_MAP = {
    "happy": ["love", "great", "amazing", "good", "excellent", "😊", "😄", "😍"],
    "angry": ["hate", "worst", "terrible", "bad", "poor", "😠", "😡"],
    "frustrated": ["slow", "lag", "issue", "problem", "😤"],
    "neutral": []
}

# -----------------------------
# CLEAN WORDS
# -----------------------------
def extract_words(text):
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

# -----------------------------
# GET TOP KEYWORDS
# -----------------------------
def get_top_keywords(df, sentiment="negative", n=10):
    df_filtered = df[df["sentiment"] == sentiment]

    all_words = []
    for text in df_filtered["text"]:
        all_words.extend(extract_words(str(text)))

    counter = Counter(all_words)
    return counter.most_common(n)

# -----------------------------
# EMOTION DETECTION
# -----------------------------
def detect_emotions(df):
    emotion_counts = Counter()

    for text in df["text"]:
        text = str(text).lower()

        for emotion, keywords in EMOTION_MAP.items():
            for kw in keywords:
                if kw in text:
                    emotion_counts[emotion] += 1

    return dict(emotion_counts)