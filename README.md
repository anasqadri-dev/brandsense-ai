# BrandSense AI

## Real-Time Sentiment Analysis for Brand Perception on X (Twitter)

---

## 📌 Project Overview

BrandSense AI is a Machine Learning project developed for the CSC-350 Artificial Intelligence course at Sukkur IBA University.

The system analyzes public sentiment regarding Pakistani telecom brands using tweets collected from X (Twitter).

The application:

- Collects tweets using the Twitter API
- Uses synthetic data as fallback when API fails
- Cleans and preprocesses text data
- Trains a Machine Learning model using TF-IDF + Logistic Regression
- Predicts sentiment in real-time
- Visualizes brand perception using interactive charts

---

## 👨‍💻 Team Members

- **Anas**
- **Shaheer**
- **Sumera**

---

## 🎓 Course Information

| Field       | Details                         |
| ----------- | ------------------------------- |
| Course      | CSC-350 Artificial Intelligence |
| Semester    | Spring 2026                     |
| Instructor  | Maham Hadi                      |
| Institution | Sukkur IBA University           |

---

## 🧠 Features

- ✅ Real-time tweet collection using Twitter API
- ✅ Automatic fallback to synthetic data generation
- ✅ Sentiment Analysis (Positive / Negative / Neutral)
- ✅ TF-IDF Vectorization
- ✅ Logistic Regression Model
- ✅ Interactive Streamlit Dashboard
- ✅ Sentiment Trend Visualization
- ✅ Keyword & Emotion Insights
- ✅ Brand Comparison Scores
- ✅ CSV Data Export

---

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Tweepy
- Streamlit
- Plotly
- Matplotlib
- Joblib

---

## 📁 Project Structure

```bash
brandsense-ai/
├── data
├── models
├── src
│   ├── brand_analysis.py
│   ├── data_generator.py
│   ├── insights.py
│   ├── predict.py
│   ├── preprocess.py
│   ├── scraper.py
│   └── train.py
├── app.py
├── README.md
└── requirments.txt
```

---

# ⚙️ Installation & Setup

**Option A: If using GitHub**

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/anasqadri-dev/brandsense-ai.git
```

---

**Option B: If you have the zip folder**

```bash
Extract the zip file to your computer
```

Open the project folder:

```bash
cd brandsense-ai
```

## 📦 Install Required Libraries

Run:

```bash
pip install -r requirments.txt
```

---

## 🔑 Configure Twitter API

Create a file named:

```bash
.env
```

Add your Twitter Developer credentials:

```env
BEARER_TOKEN=your_bearer_token_here
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
```

---

# 🐦 Step 1 — Collect Tweets

Run the scraper:

```bash
python src/scraper.py
```

The system will:

- Fetch tweets from Twitter API
- Save them inside:

```bash
data/tweets.csv
```

> ⚠️ If the Twitter API does not return tweets, the system automatically switches to synthetic data generation.

---

# 🤖 Step 2 — Train the Machine Learning Model

Run:

```bash
python src/train.py
```

This step will:

- Clean tweet text
- Convert text into TF-IDF features
- Train Logistic Regression model
- Save trained files inside:

```bash
models/model.pkl
models/vectorizer.pkl
```

The terminal will also display:

- Model Accuracy
- Classification Report

---

# 🚀 Step 3 — Launch the Dashboard

Run:

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at:

```bash
http://localhost:8501
```

---

# 📊 Dashboard Features

## 📈 Sentiment Distribution

Visual breakdown of:

- Positive tweets
- Negative tweets
- Neutral tweets

---

## 📅 Sentiment Trend Over Time

Daily trend analysis of sentiment changes.

---

## 🔮 Real-Time Prediction

Users can enter any sentence or tweet and instantly receive:

- Sentiment prediction
- Confidence score

---

## 🔍 Keyword Insights

Displays:

- Most common complaints
- Most common praises

---

## 😊 Emotion Analysis

Detects emotions such as:

- Happy
- Angry
- Frustrated

---

## 🏆 Brand Comparison

Compares Pakistani telecom brands using sentiment scores.

---

## 📥 Data Export

Filtered tweet data can be downloaded as CSV.

---

# 🧪 Example Input

```text
Jazz internet is amazing! Super fast speeds 👍
```

## Example Output

```text
😊 POSITIVE
Confidence: 98%
```

---

# 📊 Machine Learning Details

| Component          | Technique                 |
| ------------------ | ------------------------- |
| Text Cleaning      | Regex-based preprocessing |
| Feature Extraction | TF-IDF                    |
| ML Algorithm       | Logistic Regression       |
| Task               | Sentiment Classification  |

---

# 🧠 Sentiment Classes

The model predicts:

- Positive 😊
- Negative 😠
- Neutral 😐

---

# 📂 Generated Files

After running the project:

| File                    | Purpose                    |
| ----------------------- | -------------------------- |
| `data/tweets.csv`       | Collected/generated tweets |
| `models/model.pkl`      | Trained ML model           |
| `models/vectorizer.pkl` | TF-IDF vectorizer          |

---

# ⚠️ Important Notes

- Internet connection is required for Twitter API access.
- If API access fails, synthetic data is generated automatically.
- The project is intended for academic use only.

---

# 🏁 Future Improvements

Possible future enhancements:

- Deep Learning models
- Multi-language sentiment analysis
- Live streaming tweets
- Deployment on cloud platforms
- Advanced analytics dashboard

---

# ❤️ Acknowledgment

Special thanks to:

- Sukkur IBA University
- Course Instructor: Maham Hadi

for guidance and support throughout the project.

---

# 📜 License

This project is developed strictly for academic purposes under CSC-350 Artificial Intelligence.
