from transformers import pipeline
import torch # Ensure torch is imported, though it might not be directly used if pipeline handles device placement

def summarize_articles(articles_data, min_summary_length=30, max_summary_length_ratio=0.5):
    """
    Summarizes the content of a list of articles using a pre-trained model.

    Args:
        articles_data (list): A list of dictionaries, where each dictionary represents an article
                                and must contain a 'content' or 'description' key.
        min_summary_length (int): The minimum length of the generated summary.
        max_summary_length_ratio (float): The maximum length of the summary as a ratio of the
                                          original text length.

    Returns:
        list: The list of articles, with a 'summary' key added to each article dictionary.
              Returns original articles_data if model loading fails, with summaries marked unavailable.
    """
    try:
        # Using a specific model for summarization
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except Exception as e:
        print(f"Error loading summarization model: {e}")
        for article in articles_data:
            article['summary'] = 'Summarization Unavailable (model load error)'
        return articles_data

    summarized_articles = []
    for article in articles_data:
        text_to_summarize = article.get('content') or article.get('description', '') # Prioritize 'content'

        if not text_to_summarize.strip():
            article['summary'] = 'No content to summarize.'
            summarized_articles.append(article)
            continue

        try:
            # Determine max_length for the summary
            # Model's max input length (e.g., 1024 for distilbart) should be considered for input,
            # but here we set max_length for the *output* summary.
            # The pipeline handles truncation of input text if it's too long for the model.
            original_text_length = len(text_to_summarize.split()) # Rough word count
            dynamic_max_length = int(original_text_length * max_summary_length_ratio)

            # Ensure max_length is not less than min_summary_length
            # and also not excessively large (e.g., > 150-200 words for a summary is often too much)
            # Models also have their own max output length limits.
            # For "sshleifer/distilbart-cnn-12-6", max_length for output is 142 tokens by default.
            # We should respect this, or the model might truncate unexpectedly or error.
            # Let's cap dynamic_max_length to a model-sensible value if it's too high.
            # The pipeline's default max_length for this model is 142.
            # Let's allow it to be set up to that, but ensure min_length is also respected.

            summary_max_len = max(min_summary_length, dynamic_max_length)
            summary_max_len = min(summary_max_len, 140) # Cap at slightly less than model's typical max for safety

            summary_min_len = min(min_summary_length, summary_max_len -10 if summary_max_len > 40 else summary_max_len // 2)
            if summary_min_len < 0: summary_min_len = 0


            if len(text_to_summarize) < summary_min_len * 2: # If text is too short, skip summarization
                 article['summary'] = text_to_summarize # Return original text if too short
                 summarized_articles.append(article)
                 continue

            result = summarizer(text_to_summarize, max_length=summary_max_len, min_length=summary_min_len, do_sample=False)
            article['summary'] = result[0]['summary_text']
        except Exception as e:
            print(f"Error summarizing article: {article.get('title', 'Unknown Title')}. Error: {e}")
            article['summary'] = 'Summarization Failed'
        summarized_articles.append(article)

    return summarized_articles

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    sample_articles_for_summarization = [
        {
            "title": "Deep Learning Breakthroughs",
            "content": "Researchers have announced significant breakthroughs in deep learning techniques, paving the way for more accurate and efficient AI models. The new methods address long-standing challenges in training complex neural networks and are expected to have wide-ranging applications across various fields, including natural language processing, computer vision, and robotics. Experts believe these advancements will accelerate the development of truly intelligent systems. The core of the innovation lies in a novel architecture that optimizes data flow and reduces computational overhead, allowing for much larger models to be trained effectively. This will likely lead to new benchmarks in AI performance in the coming years."
        },
        {
            "title": "Short Article",
            "description": "This is a very short article. It doesn't have much content."
        },
        {
            "title": "Article with only title"
        }
    ]

    print("Original articles for summarization:")
    for art in sample_articles_for_summarization:
        print(f"- Title: {art.get('title')}, Content Hint: {art.get('content', art.get('description', 'N/A'))[:50]}...")

    summarized_sample_articles = summarize_articles(sample_articles_for_summarization, min_summary_length=20, max_summary_length_ratio=0.3)

    print("\nSummarized articles:")
    for art in summarized_sample_articles:
        print(f"- Title: {art.get('title')}, Summary: {art['summary']}")
