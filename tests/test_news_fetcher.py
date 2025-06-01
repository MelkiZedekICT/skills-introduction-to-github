import unittest
from unittest.mock import patch, MagicMock
from app.news_fetcher import fetch_news # Ensure this path is correct based on how you run tests

class TestNewsFetcher(unittest.TestCase):

    @patch('app.news_fetcher.requests.get')
    def test_fetch_news_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ok",
            "totalResults": 2,
            "articles": [
                {"title": "Test Article 1", "description": "Desc 1", "content": "Content 1", "url": "url1", "publishedAt": "date1"},
                {"title": "Test Article 2", "description": "Desc 2", "content": "Content 2", "url": "url2", "publishedAt": "date2"}
            ]
        }
        mock_get.return_value = mock_response

        articles = fetch_news(api_key="fake_key", query="test")
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]['title'], "Test Article 1")
        mock_get.assert_called_once() # Verify that requests.get was called

    @patch('app.news_fetcher.requests.get')
    def test_fetch_news_api_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200 # NewsAPI often returns 200 even for errors, with status='error' in JSON
        mock_response.json.return_value = {
            "status": "error",
            "code": "apiKeyInvalid",
            "message": "Your API key is invalid or incorrect."
        }
        mock_get.return_value = mock_response

        articles = fetch_news(api_key="invalid_key", query="test")
        self.assertEqual(len(articles), 0) # Expect an empty list on API error status

    @patch('app.news_fetcher.requests.get')
    def test_fetch_news_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500 # Internal Server Error
        mock_response.raise_for_status.side_effect = Exception("HTTP Error") # Mock that raise_for_status would trigger
        mock_get.return_value = mock_response

        articles = fetch_news(api_key="fake_key", query="test")
        self.assertEqual(len(articles), 0) # Expect an empty list on HTTP error

    def test_fetch_news_no_api_key(self):
        # Test behavior if api_key is None or empty, though routes.py checks this first.
        # The function itself might try to make a call, which would then fail.
        # Depending on implementation, this might raise an error or return empty.
        # Current fetch_news would proceed and likely get an error from the API.
        with patch('app.news_fetcher.requests.get') as mock_get_no_key:
             mock_response_no_key = MagicMock()
             mock_response_no_key.status_code = 200
             mock_response_no_key.json.return_value = {"status": "error", "message": "API key missing"}
             mock_get_no_key.return_value = mock_response_no_key

             articles = fetch_news(api_key=None, query="test")
             self.assertEqual(len(articles), 0)

if __name__ == '__main__':
    unittest.main()
