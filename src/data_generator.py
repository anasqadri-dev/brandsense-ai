import pandas as pd
import random
from datetime import datetime, timedelta

brands = ["Jazz", "Zong", "Ufone", "Telenor", "PTCL", "Nayatel"]

positive = [
    "I love {brand}, great service",
    "{brand} internet is amazing",
    "Best network is {brand}"
]

negative = [
    "{brand} is terrible",
    "Worst service ever from {brand}",
    "I hate {brand}"
]

neutral = [
    "Anyone using {brand}?",
    "How is {brand} network?",
    "{brand} vs others?"
]

def generate_data(n=500):
    data = []

    for _ in range(n):
        brand = random.choice(brands)
        sentiment = random.choice(["positive", "negative", "neutral"])

        if sentiment == "positive":
            text = random.choice(positive).format(brand=brand)
        elif sentiment == "negative":
            text = random.choice(negative).format(brand=brand)
        else:
            text = random.choice(neutral).format(brand=brand)

        data.append({
            "text": text,
            "created_at": datetime.now() - timedelta(days=random.randint(0, 10)),
            "brand": brand,
            "sentiment": sentiment
        })

    df = pd.DataFrame(data)
    df.to_csv("data/tweets.csv", index=False)

    print("✅ Synthetic data generated successfully!")

if __name__ == "__main__":
    generate_data(500)