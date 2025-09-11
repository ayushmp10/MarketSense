from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import google.generativeai as genai
import json
import yfinance as yf

load_dotenv()

app = Flask(__name__)
CORS(app)

# We no longer need NEWS_API_KEY since we're using Yahoo Finance
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Add this to your .env file

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def render_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/sentiment/<ticker>')
def analyze_sentiment(ticker):
    try:
        print(f"Analyzing sentiment for ticker: {ticker}")
        
        # Fetch news from Yahoo Finance
        news_data = fetch_yahoo_finance_news(ticker)
        
        # Since Yahoo Finance news is already ticker-specific, we can analyze directly
        if news_data.get('articles'):
            print(f"Found {len(news_data['articles'])} articles for {ticker}")
            analyzed_data = analyze_articles(news_data)
        else:
            print(f"No articles found for ticker: {ticker}")
            analyzed_data = {
                'articles': [],
                'overall_sentiment': 0,
                'article_count': 0,
                'message': f'No recent news found for ticker {ticker}. This could be due to the ticker being invalid or having no recent news coverage.'
            }
        
        return jsonify(analyzed_data)
    except Exception as e:
        print(f"Error in analyze_sentiment for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500

def fetch_yahoo_finance_news(ticker):
    """Fetch news articles from Yahoo Finance for a specific ticker"""
    try:
        # Create a yfinance ticker object
        ticker_obj = yf.Ticker(ticker)
        
        # Get news for this ticker
        news = ticker_obj.news
        
        # Convert Yahoo Finance news format to match our expected format
        articles = []
        for article in news:
            # Yahoo Finance now nests content under 'content' key
            content = article.get('content', article)  # Fallback to article itself if no content key
            
            # Handle timestamp - Yahoo Finance uses 'pubDate' in ISO format
            published_at = datetime.now(timezone.utc).isoformat()  # Default to current time
            if 'pubDate' in content and content['pubDate']:
                try:
                    # pubDate is already in ISO format
                    published_at = content['pubDate']
                except (ValueError, KeyError):
                    published_at = datetime.now(timezone.utc).isoformat()
            
            # Get thumbnail URL safely
            thumbnail_url = ''
            if content.get('thumbnail') and content['thumbnail'].get('resolutions'):
                try:
                    # Get the largest resolution available
                    resolutions = content['thumbnail']['resolutions']
                    if resolutions:
                        thumbnail_url = resolutions[-1].get('url', '')
                except (IndexError, KeyError, TypeError):
                    thumbnail_url = ''
            
            # Get the article URL
            article_url = ''
            if content.get('clickThroughUrl') and content['clickThroughUrl'].get('url'):
                article_url = content['clickThroughUrl']['url']
            elif content.get('canonicalUrl') and content['canonicalUrl'].get('url'):
                article_url = content['canonicalUrl']['url']
            
            # Get provider name
            provider_name = 'Yahoo Finance'
            if content.get('provider') and content['provider'].get('displayName'):
                provider_name = content['provider']['displayName']
            
            formatted_article = {
                'title': content.get('title', 'No title available'),
                'description': content.get('summary', content.get('description', 'No description available')),
                'url': article_url,
                'urlToImage': thumbnail_url,
                'publishedAt': published_at,
                'source': {
                    'name': provider_name
                },
                'content': content.get('summary', content.get('description', 'No content available'))
            }
            articles.append(formatted_article)
        
        print(f"Successfully fetched {len(articles)} articles for ticker {ticker}")
        return {'articles': articles}
    
    except Exception as e:
        print(f"Error fetching Yahoo Finance news for {ticker}: {e}")
        return {'articles': []}

def filter_relevant_articles(ticker, articles):
    """
    Optional additional filtering using Gemini AI.
    Since Yahoo Finance already provides ticker-specific news, this is mainly
    for additional quality filtering if needed.
    """
    # For Yahoo Finance news, we can return articles as-is since they're already relevant
    # Or optionally apply additional filtering for quality
    return articles[:15]  # Limit to 15 most recent articles

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