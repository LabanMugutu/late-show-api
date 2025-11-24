"""
Pytest fixtures: create app with in-memory sqlite and seed minimal data.
"""
import pytest
from app import create_app
from models import db as _db, Episode, Guest

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }
    app = create_app(test_config)
    with app.app_context():
        _db.create_all()
        # minimal seed
        e1 = Episode(date="1/11/99", number=1)
        e2 = Episode(date="1/12/99", number=2)
        g1 = Guest(name="Michael J. Fox", occupation="actor")
        g2 = Guest(name="Tracey Ullman", occupation="television actress")
        _db.session.add_all([e1, e2, g1, g2])
        _db.session.commit()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
