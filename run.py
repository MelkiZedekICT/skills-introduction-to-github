from app import create_app

app = create_app()

if __name__ == '__main__':
    # Port can be configured via environment variable or directly
    app.run(debug=True, host='0.0.0.0', port=5000)
