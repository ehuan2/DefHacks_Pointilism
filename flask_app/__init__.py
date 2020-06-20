from flask import Flask
from flask_app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from flask_app.main.routes import main
    
    app.register_blueprint(main)

    return app