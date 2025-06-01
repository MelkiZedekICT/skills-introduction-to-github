from flask import Blueprint, render_template, current_app
from .news_fetcher import fetch_news
from .classifier import classify_articles
from .summarizer import summarize_articles
import os # Required for getting NEWS_API_KEY from environment for safety
# Assuming config.py stores the key, but environment variable is safer for keys
# from config import NEWS_API_KEY


bp = Blueprint('main', __name__)

# Define categories for classification
NEWS_CATEGORIES = ["Technology", "Politics", "Sports", "Business", "Science", "Entertainment", "Health", "World"]

@bp.route('/')
def index():
    articles = []
    error_message = None

    # It's better to get API Key from environment variable or a secure config
    # For now, let's try to get it from config.py (which should be in .gitignore if it has real keys)
    # or directly from an environment variable.
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key or api_key == "YOUR_NEWS_API_KEY_HERE":
        # Fallback to config.py if not in env (less secure for keys)
        try:
            from config import NEWS_API_KEY as config_api_key
            if config_api_key and config_api_key != "YOUR_NEWS_API_KEY_HERE":
                api_key = config_api_key
            else:
                error_message = "News API key is not configured. Please set NEWS_API_KEY in config.py or as an environment variable."
                return render_template('index.html', articles=[], error_message=error_message)
        except ImportError:
            error_message = "Configuration file (config.py) not found or NEWS_API_KEY is missing."
            return render_template('index.html', articles=[], error_message=error_message)


    # 1. Fetch news
    raw_articles = fetch_news(api_key=api_key, query="latest OR top", language="en") # Fetch a mix

    if not raw_articles:
        error_message = "Could not fetch news articles. Check API key or network."
        # It might be that fetch_news returns an empty list on error, or raises an exception
        # The current fetch_news returns a list, so if it's empty, that's the indicator.
    else:
        # For performance, let's process a limited number of articles, e.g., top 10-20
        articles_to_process = raw_articles[:15]

        # 2. Classify articles
        # Ensure articles_to_process have 'description' or 'content' for classifier
        # The classifier handles missing text, but good to be aware
        classified_articles = classify_articles(articles_to_process, NEWS_CATEGORIES)

        # 3. Summarize articles
        # Ensure articles have 'content' or 'description' for summarizer
        articles = summarize_articles(classified_articles)

    return render_template('index.html', articles=articles, error_message=error_message)
