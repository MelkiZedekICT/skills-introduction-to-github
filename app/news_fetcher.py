import requests
import json

def fetch_news(api_key, query='world', language='en'):
    """
    Fetches news articles from the NewsAPI.

    Args:
        api_key: Your NewsAPI API key.
        query: The search query (e.g., 'bitcoin', 'politics').
               Defaults to 'world'.
        language: The language of the articles (e.g., 'en', 'es').
                  Defaults to 'en'.

    Returns:
        A list of articles, where each article is a dictionary
        containing 'title', 'description', 'content', 'url', and 'publishedAt'.
        Returns an empty list if an error occurs.
    """
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': language,
        'apiKey': api_key,
        'sortBy': 'publishedAt',  # Sort by newest first
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()

        if data.get('status') == 'ok':
            articles = []
            for article_data in data.get('articles', []):
                articles.append({
                    'title': article_data.get('title'),
                    'description': article_data.get('description'),
                    'content': article_data.get('content'),
                    'url': article_data.get('url'),
                    'publishedAt': article_data.get('publishedAt'),
                })
            return articles
        else:
            print(f"Error from NewsAPI: {data.get('message')}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response from NewsAPI")
        return []

if __name__ == '__main__':
    # This is an example of how to use the function.
    # You'll need to replace "YOUR_NEWS_API_KEY_HERE" with a real API key
    # from your config.py or environment variable to test this.
    # from config import NEWS_API_KEY # Assuming you have config.py in the same directory for testing
    # articles = fetch_news(NEWS_API_KEY, query="technology")
    # if articles:
    #     for i, article in enumerate(articles[:5]): # Print first 5 articles
    #         print(f"\n--- Article {i+1} ---")
    #         print(f"Title: {article['title']}")
    #         print(f"Description: {article['description']}")
    #         print(f"URL: {article['url']}")
    # else:
    #     print("No articles found or an error occurred.")
    pass
