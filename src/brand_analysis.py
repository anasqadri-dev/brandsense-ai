import pandas as pd

def calculate_brand_scores(df):
    """
    Calculate sentiment score for each brand
    """

    results = []

    if df.empty or "sentiment" not in df.columns or "brand" not in df.columns:
        return pd.DataFrame()

    for brand in df["brand"].unique():

        brand_df = df[df["brand"] == brand]

        total = len(brand_df)
        if total == 0:
            continue

        positive = len(brand_df[brand_df["sentiment"] == "positive"])
        negative = len(brand_df[brand_df["sentiment"] == "negative"])

        raw_score = (positive - negative) / total
        final_score = ((raw_score + 1) / 2) * 100  # normalize 0–100

        results.append({
            "brand": brand,
            "positive": positive,
            "negative": negative,
            "total": total,
            "score": round(final_score, 2)
        })

    return pd.DataFrame(results).sort_values("score", ascending=False)