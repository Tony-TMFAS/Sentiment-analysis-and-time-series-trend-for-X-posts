📊 Twitter Sentiment Analysis Dashboard

This project is my end-to-end implementation of a Twitter Sentiment Analysis Pipeline + Dashboard.
It combines a Jupyter notebook (for preprocessing, sentiment analysis, and exploration) with a Streamlit app (for interactive visualization and deployment).

Tweets were scraped using Twikit, processed in Python, and classified using the CardiffNLP RoBERTa model.

🚀 Features

Jupyter Notebook (offline analysis)

Clean & preprocess tweets (URLs, mentions, hashtags, emojis, etc.)

Run sentiment analysis using CardiffNLP RoBERTa

Save labeled dataset (tweets_labeled.csv)

Generate exploratory plots and word clouds

Streamlit Dashboard (interactive app)

KPIs: Total tweets, Positive %, Neutral %, Negative %

Sentiment distribution (histogram)

Sentiment trend over time (line chart)

Word clouds per sentiment

Sample tweets viewer

Custom text input with "Predict Sentiment" button for live inference

🛠 Tech Stack

Python

Jupyter Notebook → Preprocessing, exploration, and modeling

Streamlit → Interactive dashboard

Pandas → Data wrangling

Plotly & Matplotlib → Visualizations

WordCloud → Text visualization

Transformers (Hugging Face) → Pretrained RoBERTa sentiment model

Torch → Deep learning backend

📂 Project Structure

Sentiment analysis and time series trend for X posts.ipynb → Jupyter notebook (data processing + analysis)

tweets_labeled.csv → Example dataset (scraped & labeled tweets)

streamlit_app.py → Main Streamlit dashboard

requirements.txt → Dependencies

scraper.py for scraping tweets

tweets_labeled.csv

README.md → Project documentation

⚡ Quickstart
Option 1: Run Notebook

Open Sentiment analysis and time series trend for X posts.ipynb in Jupyter/Colab

Install required dependencies (see requirements.txt)

Run cells to preprocess tweets, classify sentiment, and generate plots

Option 2: Run Streamlit Dashboard

Clone the repository:
git clone https://github.com/your-username/twitter-sentiment-dashboard.git
cd twitter-sentiment-dashboard

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run streamlit_app.py

📊 Example Outputs

Notebook → Sentiment-labeled dataset, static visualizations (distribution, trends, word clouds)

Streamlit App → Interactive dashboard with KPIs, filters, and live sentiment prediction

🌐 Deployment

This project can be deployed easily on Streamlit Cloud:

Push the repo to GitHub

Go to share.streamlit.io
 and connect your repo

Add requirements.txt

Deploy 🚀

🔮 Future Improvements

Real-time tweet scraping instead of static CSV

Multi-language sentiment support

Topic modeling / keyword clustering

Weighted word clouds (TF-IDF instead of raw counts)

✨ Why I Built This

I wanted to combine data science exploration (via Jupyter notebook) with an interactive web dashboard (via Streamlit).
This workflow helped me practice:

Data preprocessing & NLP pipelines

Using Hugging Face transformers in real projects

Building dashboards for non-technical users

Turning scraped data into actionable insights

This project is both a portfolio piece and a practical tool for sentiment tracking.
