import unittest
from unittest.mock import patch, MagicMock
from app.summarizer import summarize_articles

class TestSummarizer(unittest.TestCase):

    @patch('app.summarizer.pipeline')
    def test_summarize_articles_success(self, mock_pipeline):
        mock_summarizer_instance = MagicMock()
        # Simulate summarization results
        mock_summarizer_instance.side_effect = [
            [{'summary_text': 'Short summary for article 1.'}],
            [{'summary_text': 'Brief recap of article 2.'}],
        ]
        mock_pipeline.return_value = mock_summarizer_instance

        articles_data = [
            {"title": "Long Article 1", "content": "This is a very long text for article 1 that needs summarization..."},
            {"title": "Medium Article 2", "description": "Some text for article 2..."}
        ]

        summarized = summarize_articles(articles_data)

        self.assertEqual(len(summarized), 2)
        self.assertEqual(summarized[0]['summary'], 'Short summary for article 1.')
        self.assertEqual(summarized[1]['summary'], 'Brief recap of article 2.')
        mock_pipeline.assert_called_once_with("summarization", model="sshleifer/distilbart-cnn-12-6")

    @patch('app.summarizer.pipeline')
    def test_summarize_articles_model_load_error(self, mock_pipeline):
        mock_pipeline.side_effect = Exception("Model load failed")
        articles_data = [{"title": "Test", "content": "Test content"}]

        summarized = summarize_articles(articles_data)
        self.assertEqual(summarized[0]['summary'], 'Summarization Unavailable (model load error)')

    def test_summarize_articles_empty_input(self):
        summarized = summarize_articles([])
        self.assertEqual(len(summarized), 0)

    @patch('app.summarizer.pipeline')
    def test_summarize_articles_no_content(self, mock_pipeline):
        mock_summarizer_instance = MagicMock() # Won't be called
        mock_pipeline.return_value = mock_summarizer_instance
        articles_data = [{"title": "No Content Article"}] # No 'content' or 'description'

        summarized = summarize_articles(articles_data)
        self.assertEqual(summarized[0]['summary'], 'No content to summarize.')
        # mock_summarizer_instance.assert_not_called()

    @patch('app.summarizer.pipeline')
    def test_summarize_article_too_short_for_summary(self, mock_pipeline):
        mock_summarizer_instance = MagicMock()
        mock_pipeline.return_value = mock_summarizer_instance

        short_content = "Too short."
        articles_data = [{"title": "Short", "content": short_content}]

        # min_summary_length default is 30. If content is shorter than min_summary_length * 2 (approx)
        # it returns original text.
        summarized = summarize_articles(articles_data, min_summary_length=10)
        self.assertEqual(summarized[0]['summary'], short_content) # Expect original text
        # mock_summarizer_instance.assert_not_called() # Check pipeline wasn't called

if __name__ == '__main__':
    unittest.main()
