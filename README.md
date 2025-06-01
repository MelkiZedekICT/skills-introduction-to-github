# AI-Powered News Aggregator

This application fetches news articles from a public API, classifies them by topic using AI,
summarizes long articles, and displays the results in a simple web interface.

## Features

- Fetches live news articles (via NewsAPI).
- Classifies articles into categories (e.g., Technology, Politics, Sports).
- Summarizes articles using NLP.
- Simple Flask web interface to display news.

## Project Structure

```
.
├── app/                  # Main application package
│   ├── __init__.py       # Application factory
│   ├── classifier.py     # Article classification module
│   ├── news_fetcher.py   # News fetching module
│   ├── routes.py         # Flask routes
│   └── summarizer.py     # Article summarization module
├── static/               # Static files (CSS, JS)
│   └── css/
│       └── style.css
├── templates/            # HTML templates
│   ├── index.html
│   └── layout.html
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_classifier.py
│   ├── test_news_fetcher.py
│   └── test_summarizer.py
├── config.py             # Configuration (e.g., API key)
├── requirements.txt      # Python dependencies
├── run.py                # Script to run the Flask application
└── README.md             # This file
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create a Python virtual environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install Flask, requests, transformers, and PyTorch (torch).
    *Note: Installing PyTorch can sometimes be memory intensive. If you encounter issues, you might need to install it separately following instructions from the [official PyTorch website](https://pytorch.org/get-started/locally/) that best suit your system.*

4.  **Configure the NewsAPI Key:**
    - Obtain a free API key from [NewsAPI.org](https://newsapi.org/).
    - Open the `config.py` file in the project root.
    - Replace `"YOUR_NEWS_API_KEY_HERE"` with your actual NewsAPI key:
      ```python
      NEWS_API_KEY = "YOUR_ACTUAL_NEWS_API_KEY"
      ```
    - **Alternatively (and more securely for production/sharing)**, you can set it as an environment variable:
      ```bash
      export NEWS_API_KEY="YOUR_ACTUAL_NEWS_API_KEY" # On Linux/macOS
      # set NEWS_API_KEY="YOUR_ACTUAL_NEWS_API_KEY" # On Windows (cmd)
      # $env:NEWS_API_KEY="YOUR_ACTUAL_NEWS_API_KEY" # On Windows (PowerShell)
      ```
      The application will first try to load the key from the environment variable.

## Running the Application

1.  **Ensure your virtual environment is activated.**
2.  **Run the Flask development server:**
    ```bash
    python run.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:5000/` (or `http://0.0.0.0:5000/`).

The first time you run the application, the AI models for classification and summarization will be downloaded. This might take some time and requires an internet connection. Subsequent runs will use the cached models.

## Running Unit Tests

1.  **Ensure your virtual environment is activated and dependencies are installed.**
2.  **Navigate to the project root directory.**
3.  **Run the tests using Python's `unittest` module:**
    ```bash
    python -m unittest discover tests
    ```
    This will automatically find and run all tests within the `tests` directory.

## Notes

- The AI models used (especially for classification and summarization) can be resource-intensive. Performance will vary depending on your hardware.
- The application fetches a limited number of recent articles (around 15) for processing to keep response times reasonable for a demo.
- For simplicity, this application does not use a database. News is fetched and processed on each request to the homepage. For a production application, caching strategies and background tasks would be necessary.

```
