import tweepy
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
# At the top of scraper.py, add this import for synthetic fallback
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load API keys
load_dotenv()

client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    wait_on_rate_limit=True
)

brands = ["Jazz", "Zong", "Ufone", "Telenor", "PTCL", "Nayatel"]

def fetch_tweets(query, max_results=50):
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics", "text"]
        )

        data = []

        if tweets.data:
            for tweet in tweets.data:
                metrics = tweet.public_metrics

                data.append({
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "likes": metrics["like_count"],
                    "retweets": metrics["retweet_count"],
                    "brand": query,
                    "fetched_at": datetime.now()
                })

        return data

    except Exception as e:
        print(f"Error fetching {query}:", e)
        return []


def run_scraper():
    all_tweets = []

    for brand in brands:
        print(f"Fetching tweets for {brand}...")

        query = f"{brand} -is:retweet lang:en"
        tweets = fetch_tweets(query)

        all_tweets.extend(tweets)

    df = pd.DataFrame(all_tweets)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/tweets.csv", index=False)

    print("\n✅ Data collection complete!")
    print(f"Total tweets collected: {len(df)}")

    # ✅ FIXED: fallback logic
    if len(df) == 0:
        print("\n⚠️ No tweets from API. Switching to synthetic data...\n")

        # correct import (depends on your structure)
        try:
            from src.data_generator import generate_data
        except:
            from data_generator import generate_data

        generate_data()


if __name__ == "__main__":
    run_scraper()