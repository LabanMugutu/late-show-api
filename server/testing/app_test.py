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

def test_get_guests(client):
    resp = client.get("/guests")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert 'id' in data[0] and 'name' in data[0]

def test_post_appearance_success(client):
    eps = client.get("/episodes").get_json()
    gs = client.get("/guests").get_json()
    ep_id = eps[0]['id']
    guest_id = gs[0]['id']
    payload = {'rating': 5, 'episode_id': ep_id, 'guest_id': guest_id}
    resp = client.post("/appearances", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['rating'] == 5
    assert data['episode_id'] == ep_id
    assert data['guest_id'] == guest_id
    assert 'episode' in data and 'guest' in data

def test_post_appearance_validation_error_missing_fields(client):
    payload = {'rating': 5}
    resp = client.post("/appearances", json=payload)
    assert resp.status_code == 400
    assert 'errors' in resp.get_json()

def test_post_appearance_validation_error_invalid_rating(client):
    eps = client.get("/episodes").get_json()
    gs = client.get("/guests").get_json()
    ep_id = eps[0]['id']
    guest_id = gs[0]['id']
    payload = {'rating': 10, 'episode_id': ep_id, 'guest_id': guest_id}
    resp = client.post("/appearances", json=payload)
    assert resp.status_code == 400
    assert 'errors' in resp.get_json()

def test_delete_episode_success(client):
    # create and delete an episode
    with client.application.app_context():
        ep = Episode(date='9/9/99', number=999)
        db.session.add(ep)
        db.session.commit()
        eid = ep.id
    resp = client.delete(f"/episodes/{eid}")
    assert resp.status_code == 204
    assert client.get(f"/episodes/{eid}").status_code == 404

