# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="Twitter Sentiment Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# LOAD DATA
# --------------------------


@st.cache_data
def load_data():
    df_twt = pd.read_csv("tweets_labeled.csv", parse_dates=["created_at"])
    df_twt["date"] = pd.to_datetime(df_twt["created_at"]).dt.date

    # enforce consistent sentiment order
    sentiment_order = ["positive", "neutral", "negative"]
    df_twt["sentiment"] = pd.Categorical(
        df_twt["sentiment"], categories=sentiment_order, ordered=True
    )
    return df_twt


df_twt = load_data()

# --------------------------
# SIDEBAR CONTROLS
# --------------------------
st.sidebar.header("🔍 Filters")

sentiments = st.sidebar.multiselect(
    "Select Sentiment",
    options=["positive", "neutral", "negative"],  # fixed order
    default=["positive", "neutral", "negative"]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df_twt["date"].min(), df_twt["date"].max()]
)

df_filtered = df_twt[
    (df_twt["sentiment"].isin(sentiments)) &
    (df_twt["date"].between(date_range[0], date_range[1]))
]

# --------------------------
# MAIN DASHBOARD
# --------------------------
st.title("📊 Twitter Sentiment Analysis Dashboard")
st.markdown("""
This dashboard analyzes tweets scraped with **Twikit**  
and classified using **CardiffNLP RoBERTa** for sentiment.
""")

# ---- KPIs (4 columns in fixed order) ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tweets", len(df_filtered))
col2.metric("Positive %", round(
    (df_filtered["sentiment"].eq("positive").mean())*100, 1))
col3.metric("Neutral %", round(
    (df_filtered["sentiment"].eq("neutral").mean())*100, 1))
col4.metric("Negative %", round(
    (df_filtered["sentiment"].eq("negative").mean())*100, 1))

# ---- Sentiment Distribution ----
st.subheader("📌 Sentiment Distribution")
fig = px.histogram(
    df_filtered,
    x="sentiment",
    color="sentiment",
    title="Distribution of Sentiments",
    category_orders={"sentiment": ["positive", "neutral", "negative"]},
    color_discrete_map={
        "positive": "green",
        "neutral": "gray",
        "negative": "red"
    }
)
st.plotly_chart(fig, use_container_width=True)

# ---- Time Series ----
st.subheader("📈 Sentiment Trend Over Time")
sentiment_trend = df_filtered.groupby(
    ["date", "sentiment"]).size().reset_index(name="count")
fig = px.line(
    sentiment_trend,
    x="date", y="count", color="sentiment",
    title="Sentiment Over Time",
    category_orders={"sentiment": ["positive", "neutral", "negative"]},
    color_discrete_map={
        "positive": "green",
        "neutral": "gray",
        "negative": "red"
    }
)
st.plotly_chart(fig, use_container_width=True)

# ---- Word Cloud ----
st.subheader("☁️ WordCloud per Sentiment")
stopwords = set(STOPWORDS)
sent_choice = st.selectbox("Select Sentiment for WordCloud", [
                           "positive", "neutral", "negative"])

text = " ".join(df_filtered[df_filtered["sentiment"]
                == sent_choice]["clean_text"])
if text.strip():
    wc = WordCloud(width=800, height=400, background_color="white",
                   stopwords=stopwords, collocations=False).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.warning("No tweets available for this sentiment in the selected filters.")

# ---- Sample Tweets ----
st.subheader("📝 Sample Tweets")
st.dataframe(df_filtered[["created_at", "text", "sentiment"]].head(20))

# --------------------------
# EXTRA: Custom Text Inference
# --------------------------
st.subheader("🤖 Try It Yourself: Sentiment Prediction")
user_input = st.text_area("Enter a tweet or sentence to analyze:")

if user_input:
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipeline = pipeline(
        "sentiment-analysis", model=model, tokenizer=tokenizer)

    result = sentiment_pipeline(user_input[:512])[0]
    st.write(
        f"**Predicted Sentiment:** {result['label']} (Confidence: {result['score']:.2f})")
