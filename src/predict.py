"""
Prediction module for BrandSense AI
Loads trained model and predicts sentiment
"""

import joblib
from src.preprocess import clean_text


class SentimentPredictor:
    def __init__(self, model_path="models/model.pkl", vectorizer_path="models/vectorizer.pkl"):
        """Load trained model and vectorizer"""
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict(self, text):
        """Predict sentiment of a single text"""
        cleaned = clean_text(text)
        vec = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(vec)[0]

        # Confidence score
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(vec)[0]
            confidence = max(probs) * 100
        else:
            confidence = None

        return {
            "sentiment": prediction,
            "confidence": confidence,
            "original_text": text,
            "cleaned_text": cleaned
        }


# Test
if __name__ == "__main__":
    predictor = SentimentPredictor()

    test_texts = [
        "I love Jazz, great service!",
        "Zong is terrible, worst network",
        "Anyone using Ufone?"
    ]

    for text in test_texts:
        result = predictor.predict(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {result['sentiment']}")
        if result["confidence"]:
            print(f"Confidence: {result['confidence']:.1f}%")