from textblob import TextBlob
import random

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using TextBlob.
    Returns a polarity score between -1 (negative) and 1 (positive).
    """
    # In a real application, you might want to pre-process the text
    # (e.g., remove URLs, special characters) for better accuracy.
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def get_simulated_tweets(ticker):
    """
    Returns a list of simulated tweets and their sentiment for a given ticker.
    This is a placeholder for a real Twitter API integration.
    """
    # Sample tweets, mixing positive, negative, and neutral statements
    positive_tweets = [
        f"🚀 Just bought more ${ticker}! To the moon! 🌕 #stonks",
        f"Great earnings report from ${ticker}. Very bullish on this one. #investing",
        f"Loving the new product launch from ${ticker}. This company is a winner.",
        f"I think ${ticker} is seriously undervalued. A great long-term hold."
    ]
    negative_tweets = [
        f"Is anyone else concerned about ${ticker}'s latest numbers? Looks bearish to me. #trading",
        f"Just sold all my ${ticker} shares. Too much uncertainty in the market.",
        f"Disappointing guidance from ${ticker}'s management. I'm out.",
        f"The competition is crushing ${ticker}. I don't see a path forward."
    ]
    neutral_tweets = [
        f"${ticker} is trading flat today on high volume.",
        f"Upcoming Fed meeting could impact ${ticker} and the broader market.",
        f"Just a reminder that ${ticker} reports earnings next week."
    ]

    all_tweets = positive_tweets + negative_tweets + neutral_tweets

    # Randomly sample a few tweets to simulate a live feed
    num_tweets = min(len(all_tweets), 5)
    sampled_tweets = random.sample(all_tweets, num_tweets)

    results = []
    for tweet in sampled_tweets:
        polarity = analyze_sentiment(tweet)
        if polarity > 0.1:
            sentiment = "Positivo"
        elif polarity < -0.1:
            sentiment = "Negativo"
        else:
            sentiment = "Neutral"
        results.append({"tweet": tweet, "sentiment": sentiment, "polarity": polarity})

    return results
