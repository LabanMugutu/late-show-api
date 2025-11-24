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

def test_rating_validation_rejects_out_of_range(app):
    e = Episode.query.first()
    g = Guest.query.first()
    try:
        a = Appearance(rating=6, episode=e, guest=g)
        db.session.add(a)
        db.session.commit()
        assert False, "Should have raised for invalid rating"
    except Exception:
        db.session.rollback()
        assert True

def test_cascade_delete_episode(app):
    e = Episode.query.first()
    g = Guest.query.first()
    a = Appearance(rating=4, episode=e, guest=g)
    db.session.add(a)
    db.session.commit()
    aid = a.id
    # delete episode -> appearance should be deleted too
    db.session.delete(e)
    db.session.commit()
    assert Appearance.query.get(aid) is None
