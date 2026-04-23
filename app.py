"""
BrandSense AI - Streamlit Dashboard
Real-time sentiment analysis for brand perception
"""

import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import plotly.express as px
import re
from datetime import datetime

# Page config
st.set_page_config(
    page_title="BrandSense AI",
    page_icon="🐦",
    layout="wide"
)

# -----------------------------
# LOAD MODEL & VECTORIZER
# -----------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("models/model.pkl")
        vectorizer = joblib.load("models/vectorizer.pkl")
        return model, vectorizer
    except FileNotFoundError:
        st.error("⚠️ Model not found! Please run: python src/train.py")
        return None, None

# -----------------------------
# CLEAN FUNCTION
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/tweets.csv")
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"])
        return df
    except FileNotFoundError:
        st.warning("⚠️ No data found! Run scraper or data_generator first.")
        return pd.DataFrame()

# -----------------------------
# TITLE
# -----------------------------
st.markdown("# 🐦 BrandSense AI")
st.markdown("*Real-Time Sentiment Analysis for Brand Perception on X (Twitter)*")
st.markdown("---")

# Load assets
model, vectorizer = load_model()
df = load_data()

# -----------------------------
# SIDEBAR - FILTERS
# -----------------------------
with st.sidebar:
    st.markdown("## 📊 Filters")
    
    if not df.empty and "brand" in df.columns:
        brands = ["All"] + list(df["brand"].unique())
        selected_brand = st.selectbox("Select Brand", brands)
    else:
        selected_brand = "All"
        st.info("No data available for filtering")
    
    st.markdown("---")
    st.markdown("### About")
    st.info(
        "**BrandSense AI** analyzes public sentiment for Pakistani telecom brands.\n\n"
        "Built with: Logistic Regression + TF-IDF\n\n"
        "Course: CSC-350 Artificial Intelligence\n\n"
        "Team: Anas, Shaheer, Sumera"
    )

# -----------------------------
# MAIN CONTENT - 2 COLUMNS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sentiment Distribution")
    
    if not df.empty and "sentiment" in df.columns:
        # Apply brand filter
        df_filtered = df.copy()
        if selected_brand != "All" and "brand" in df.columns:
            df_filtered = df_filtered[df_filtered["brand"] == selected_brand]
        
        counts = df_filtered["sentiment"].value_counts()
        
        # Use Plotly for better visuals
        fig = px.pie(
            values=counts.values,
            names=counts.index,
            color=counts.index,
            color_discrete_map={
                "positive": "#28a745",
                "negative": "#dc3545",
                "neutral": "#ffc107"
            },
            title=f"Sentiment Breakdown for {selected_brand}"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No sentiment data available")

with col2:
    st.subheader("📊 Key Metrics")
    
    if not df.empty and "sentiment" in df.columns:
        df_filtered = df.copy()
        if selected_brand != "All" and "brand" in df.columns:
            df_filtered = df_filtered[df_filtered["brand"] == selected_brand]
        
        total = len(df_filtered)
        positive = len(df_filtered[df_filtered["sentiment"] == "positive"])
        negative = len(df_filtered[df_filtered["sentiment"] == "negative"])
        neutral = len(df_filtered[df_filtered["sentiment"] == "neutral"])
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Total Tweets", total)
        with col_b:
            pos_pct = (positive/total*100) if total > 0 else 0
            st.metric("Positive", f"{pos_pct:.1f}%", delta="😊")
        with col_c:
            neg_pct = (negative/total*100) if total > 0 else 0
            st.metric("Negative", f"{neg_pct:.1f}%", delta="😠")
    else:
        st.warning("No metrics available")

# -----------------------------
# SENTIMENT TREND
# -----------------------------
st.subheader("📅 Sentiment Trend Over Time")

if not df.empty and "created_at" in df.columns and "sentiment" in df.columns:
    df_filtered = df.copy()
    if selected_brand != "All" and "brand" in df.columns:
        df_filtered = df_filtered[df_filtered["brand"] == selected_brand]
    
    # Group by date and sentiment
    df_trend = df_filtered.groupby([pd.Grouper(key="created_at", freq="D"), "sentiment"]).size().unstack().fillna(0)
    
    if not df_trend.empty:
        fig = px.line(df_trend, title=f"Daily Sentiment Trends - {selected_brand}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data for trend visualization")
else:
    st.info("Date or sentiment data not available")

st.markdown("---")

# -----------------------------
# REAL-TIME PREDICTION
# -----------------------------
st.subheader("🔮 Real-Time Sentiment Predictor")

col_input, col_output = st.columns([2, 1])

with col_input:
    user_text = st.text_area(
        "Enter a tweet or sentence to analyze:",
        placeholder="e.g., Jazz internet is amazing! Super fast speeds 👍",
        height=100
    )
    
    analyze_button = st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True)

with col_output:
    if analyze_button and user_text:
        if model and vectorizer:
            cleaned = clean_text(user_text)
            vec = vectorizer.transform([cleaned])
            prediction = model.predict(vec)[0]
            
            # Get confidence if available
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(vec)[0]
                confidence = max(probs) * 100
            else:
                confidence = None
            
            # Display result
            if prediction == "positive":
                st.success(f"### 😊 POSITIVE")
            elif prediction == "negative":
                st.error(f"### 😠 NEGATIVE")
            else:
                st.warning(f"### 😐 NEUTRAL")
            
            if confidence:
                st.metric("Confidence", f"{confidence:.1f}%")
        else:
            st.error("Model not loaded. Please train first.")
    elif analyze_button:
        st.warning("Please enter some text to analyze")

# -----------------------------
# RECENT TWEETS
# -----------------------------
st.markdown("---")
st.subheader("📝 Recent Tweets")

if not df.empty:
    df_filtered = df.copy()
    if selected_brand != "All" and "brand" in df.columns:
        df_filtered = df_filtered[df_filtered["brand"] == selected_brand]
    
    recent = df_filtered.sort_values("created_at" if "created_at" in df.columns else "text", ascending=False).head(10)
    
    for _, tweet in recent.iterrows():
        sentiment = tweet.get("sentiment", "neutral")
        emoji = "😊" if sentiment == "positive" else "😠" if sentiment == "negative" else "😐"
        color = "#28a745" if sentiment == "positive" else "#dc3545" if sentiment == "negative" else "#ffc107"
        brand = tweet.get("brand", "Unknown")
        date = tweet.get("created_at", datetime.now())
        
        st.markdown(
            f"""
            <div style="padding: 10px; border-left: 5px solid {color}; margin: 10px 0; background-color: #f8f9fa; border-radius: 5px;">
                <small>{date} | {brand}</small>
                <p style="margin: 5px 0;">{tweet['text'][:150]}...</p>
                <strong style="color: {color};">{emoji} {sentiment.upper()}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No tweets to display")

#users can export data for analysis
# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
st.markdown("---")
st.subheader("📥 Export Data")

if not df.empty:
    df_filtered = df.copy()
    if selected_brand != "All" and "brand" in df.columns:
        df_filtered = df_filtered[df_filtered["brand"] == selected_brand]
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📊 Download Filtered Data as CSV",
        data=csv,
        file_name=f"brandsense_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown(
    "<center>Built with ❤️ for CSC-350 Artificial Intelligence | Sukkur IBA University | Spring 2026</center>",
    unsafe_allow_html=True
)