from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

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

if __name__ == '__main__':
    app.run(debug=True)