from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)

    # Default config (SQLite file)
    app.config.from_object("app.config.Config")

    # Override with testing config if provided
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
