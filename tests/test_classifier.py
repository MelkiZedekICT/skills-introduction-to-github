import unittest
from unittest.mock import patch, MagicMock
from app.classifier import classify_articles

class TestClassifier(unittest.TestCase):

    @patch('app.classifier.pipeline')
    def test_classify_articles_success(self, mock_pipeline):
        # Mock the pipeline object and its return value
        mock_classifier_instance = MagicMock()
        # Simulate classification results
        mock_classifier_instance.side_effect = [
            {'labels': ['Technology'], 'scores': [0.9]},
            {'labels': ['Sports'], 'scores': [0.85]},
        ]
        mock_pipeline.return_value = mock_classifier_instance

        articles_data = [
            {"title": "Tech Advances", "description": "New AI breakthroughs."},
            {"title": "Big Game Tonight", "description": "Local team plays for championship."}
        ]
        categories = ["Technology", "Sports", "Politics"]

        classified = classify_articles(articles_data, categories)

        self.assertEqual(len(classified), 2)
        self.assertEqual(classified[0]['category'], 'Technology')
        self.assertEqual(classified[1]['category'], 'Sports')
        mock_pipeline.assert_called_once_with("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

    @patch('app.classifier.pipeline')
    def test_classify_articles_model_load_error(self, mock_pipeline):
        mock_pipeline.side_effect = Exception("Model load failed")
        articles_data = [{"title": "Test", "description": "Test desc"}]
        categories = ["Category1"]

        classified = classify_articles(articles_data, categories)
        self.assertEqual(classified[0]['category'], 'Classification Unavailable')

    def test_classify_articles_empty_input(self):
        # No mocking needed as it should handle empty list before model use
        classified = classify_articles([], ["Technology"])
        self.assertEqual(len(classified), 0)

    @patch('app.classifier.pipeline')
    def test_classify_articles_empty_text(self, mock_pipeline):
        mock_classifier_instance = MagicMock() # Won't be called for empty text
        mock_pipeline.return_value = mock_classifier_instance

        articles_data = [{"title": " ", "description": " "}]
        categories = ["Technology"]
        classified = classify_articles(articles_data, categories)
        self.assertEqual(classified[0]['category'], 'Uncategorized')
        # mock_classifier_instance.assert_not_called() # Check it wasn't called for this case

if __name__ == '__main__':
    unittest.main()
