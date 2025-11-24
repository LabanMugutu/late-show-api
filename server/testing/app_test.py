"""
Integration tests for endpoints ensuring correct JSON shape & HTTP statuses.
"""
import json
from models import Episode, Guest, Appearance, db

def test_get_episodes(client):
    resp = client.get("/episodes")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert 'id' in data[0] and 'date' in data[0] and 'number' in data[0]

def test_get_episode_not_found(client):
    resp = client.get("/episodes/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "Episode not found"}

def test_get_episode_with_appearances(client):
    # add appearance
    with client.application.app_context():
        ep = Episode.query.first()
        g = Guest.query.first()
        a = Appearance(rating=4, episode=ep, guest=g)
        db.session.add(a)
        db.session.commit()
    resp = client.get(f"/episodes/{ep.id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'appearances' in data
    assert isinstance(data['appearances'], list)
    assert 'guest' in data['appearances'][0]
    assert 'id' in data['appearances'][0]['guest']
