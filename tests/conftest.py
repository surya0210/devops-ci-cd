# tests/conftest.py
import pytest
from sqlalchemy.pool import StaticPool
from app import create_app, db as _db

@pytest.fixture(scope="session")
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        },
    }
    app = create_app(test_config)
    with app.app_context():
        _db.create_all()
    yield app
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
        _db.engine.dispose()

@pytest.fixture(autouse=True)
def _app_ctx(app):
    """Push an app context for every test."""
    ctx = app.app_context()
    ctx.push()
    try:
        yield
    finally:
        _db.session.remove()
        ctx.pop()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def db(app):
    return _db
