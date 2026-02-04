from app.app import create_app

app = create_app()

if __name__ == "__main__":
    # This block is for local development with `python wsgi.py`
    # However, production should use `gunicorn` or `waitress-serve`
    app.run()
