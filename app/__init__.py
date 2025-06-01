from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Configuration settings could be loaded here, e.g., from config.py
    # For NewsAPI key specifically, it's better to load it where it's used (news_fetcher)
    # but global app configs can go here.
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key')
    # Example: Load other configurations if needed
    # app.config.from_object('config.Config')

    # Import and register blueprints or routes here
    from . import routes
    app.register_blueprint(routes.bp) # Assuming routes are in a blueprint

    return app
