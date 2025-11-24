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