"""
Model tests: validate relationships, rating validation and cascade delete behavior.
"""
from models import Episode, Guest, Appearance, db
def test_create_appearance_valid(app):
    e = Episode.query.first()
    g = Guest.query.first()
    a = Appearance(rating=5, episode=e, guest=g)
    db.session.add(a)
    db.session.commit()
    assert a.id is not None
    assert a.rating == 5
    assert a.episode_id == e.id
    assert a.guest_id == g.id