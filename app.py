from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime
from dotenv import load_dotenv  # Add this import

load_dotenv()  # Add this line

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # Environment variable

@app.route('/api/sentiment/<ticker>')
def analyze_sentiment(ticker):
    try:
        # Fetch news from NewsAPI
        news_data = fetch_news(ticker)
        
        # Analyze sentiment (you could use NLTK, TextBlob, or Transformers)
        analyzed_data = analyze_articles(news_data)
        
        # Optional: Store in database
        # store_analysis(ticker, analyzed_data)
        
        return jsonify(analyzed_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def fetch_news(ticker):
    url = f"https://newsapi.org/v2/everything"
    params = {
        'q': f'{ticker} AND (stock OR earnings OR financial)',
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': 20,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def analyze_articles(news_data):
    try:
        from textblob import TextBlob
    except ImportError:
        return simple_sentiment_fallback(news_data)
    
    articles = news_data.get('articles', [])
    analyzed_articles = []
    sentiment_scores = []
    
    for article in articles:
        title = article.get('title', '') or ''
        description = article.get('description', '') or ''
        combined_text = f"{title} {description}"
        
        if combined_text.strip():
            blob = TextBlob(combined_text)
            sentiment_score = blob.sentiment.polarity
        else:
            sentiment_score = 0
        
        analyzed_articles.append({
            **article,
            'sentiment': {
                'score': sentiment_score,
                'label': get_sentiment_label(sentiment_score)
            }
        })
        
        sentiment_scores.append(sentiment_score)
    
    overall_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    
    return {
        'articles': analyzed_articles,
        'overall_sentiment': overall_sentiment,
        'article_count': len(analyzed_articles)
    }

def get_sentiment_label(score):
    if score > 0.1:
        return 'positive'
    elif score < -0.1:
        return 'negative'
    else:
        return 'neutral'

def simple_sentiment_fallback(news_data):
    articles = news_data.get('articles', [])
    return {
        'articles': [
            {**article, 'sentiment': {'score': 0, 'label': 'neutral'}} 
            for article in articles
        ],
        'overall_sentiment': 0,
        'article_count': len(articles)
    }

if __name__ == '__main__':
    app.run(debug=True)