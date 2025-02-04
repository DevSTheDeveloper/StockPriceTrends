import requests
#import newspaper
import yfinance as yf
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

# Store API key
NEWS_API_KEY = "c954a0e532c24f2ab3929fa88b1ca8ac"

def get_stock_data(ticker, period="1mo"):
    """Fetches historical stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        if data.empty:
            print(f"No data found for {ticker} ({period})")
            return None
        return data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def analyze_stock_price(data):
    """Analyzes the stock price trend over time."""
    if data is None or data.empty:
        return "No stock data available", None
    
    price_changes = data['Close'].diff().sum()
    trend = "Upward" if price_changes > 0 else "Downward" if price_changes < 0 else "Neutral"
    
    price_plot = data['Close'].plot(title='Stock Price Over Time', xlabel='Date', ylabel='Closing Price')
    plt.grid()
    return f"Price trend is {trend}", price_plot.figure

def get_news_articles(query, num_articles=5):
    """Fetches news articles using NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if "articles" not in data:
            print("Error fetching news data:", data)
            return None

        return [article["content"] for article in data["articles"][:num_articles]]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def analyze_sentiment(text_list):
    """Performs sentiment analysis on news articles."""
    if text_list is None:
        return None
    
    #analyzer = SentimentIntensityAnalyzer()
    #total_score = sum(analyzer.polarity_scores(text)["compound"] for text in text_list)
    #avg_score = total_score / len(text_list) if text_list else 0

    #sentiment = "Positive" if avg_score > 0.05 else "Negative" if avg_score < -0.05 else "Neutral"
    #return {"average_compound_score": avg_score, "overall_sentiment": sentiment}

# Run Analysis
if __name__ == '__main__':
    ticker_symbol = "NVDA"
    stock_period = "6mo"
    
    # Fetch stock data
    stock_data = get_stock_data(ticker_symbol, stock_period)
    trend, plot = analyze_stock_price(stock_data)
    print(f"{ticker_symbol} Stock Trend: {trend}")
    if plot:
        plt.show()
    
    # Fetch news and analyze sentiment
    articles = get_news_articles(ticker_symbol, num_articles=5)
    sentiment = analyze_sentiment(articles) if articles else None
    if sentiment:
        print(f"Sentiment Analysis: {sentiment}")
