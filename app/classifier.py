from transformers import pipeline
import torch # Add this import

def classify_articles(articles_data, categories):
    """
    Classifies a list of articles into predefined categories using a zero-shot classification model.

    Args:
        articles_data (list): A list of dictionaries, where each dictionary represents an article
                            and must contain a 'description' or 'content' key.
        categories (list): A list of strings representing the target categories.

    Returns:
        list: The list of articles, with a 'category' key added to each article dictionary.
              Returns original articles_data if model loading or classification fails.
    """
    try:
        # Using a specific model and revision to ensure consistency
        # Using a smaller model for quicker setup, can be changed to 'facebook/bart-large-mnli'
        classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    except Exception as e:
        print(f"Error loading classification model: {e}")
        # Return articles without classification if model loading fails
        for article in articles_data:
            article['category'] = 'Classification Unavailable'
        return articles_data

    classified_articles = []
    for article in articles_data:
        text_to_classify = article.get('description') or article.get('content') or article.get('title', '')
        if not text_to_classify.strip(): # Handle empty text
            article['category'] = 'Uncategorized'
            classified_articles.append(article)
            continue
        try:
            # Ensure the input text is not excessively long for the model
            # Truncate if necessary, this depends on the model's limits
            max_length = 512 # A common limit, adjust as per model specifics
            if len(text_to_classify) > max_length:
                text_to_classify = text_to_classify[:max_length]

            result = classifier(text_to_classify, categories)
            article['category'] = result['labels'][0] # Get the category with the highest score
        except Exception as e:
            print(f"Error classifying article: {article.get('title', 'Unknown Title')}. Error: {e}")
            article['category'] = 'Classification Failed'
        classified_articles.append(article)
    return classified_articles

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    sample_articles = [
        {"title": "Tech Company Announces New AI Product", "description": "A leading tech company today unveiled a groundbreaking new artificial intelligence product that promises to revolutionize the industry."},
        {"title": "Election Results Update", "description": "The latest election results are coming in, with several key races still too close to call."},
        {"title": "Sports Team Wins Championship", "description": "The home team celebrated a stunning victory last night, clinching the championship title in a dramatic final game."},
        {"title": "Global Economic Summit Concludes", "description": "Leaders from around the world gathered to discuss pressing economic issues and potential collaborations."},
        {"description": "This is a test with only a description."}, # Test case with no title
        {"title": "Empty content article"} # Test case with no description or content
    ]
    defined_categories = ["Technology", "Politics", "Sports", "Business", "Science"]

    print("Original articles:")
    for art in sample_articles:
        print(f"- {art.get('title', art.get('description'))}")

    classified_sample_articles = classify_articles(sample_articles, defined_categories)

    print("\nClassified articles:")
    for art in classified_sample_articles:
        print(f"- Title: {art.get('title', 'N/A')}, Category: {art['category']}")
