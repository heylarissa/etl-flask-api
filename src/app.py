from flask import Flask
from src.routes import register_routes
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
