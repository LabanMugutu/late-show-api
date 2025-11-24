"""
Seed script to create initial data.

Run:
    python server/seed.py
This will create (or replace) `app.db` in project root.
"""
from app import create_app
from models import db, Episode, Guest, Appearance
app = create_app()

with app.app_context():
    # drop/create for a clean seed (safe for local dev)
    db.drop_all()
    db.create_all()

    # Episodes
    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)
    e3 = Episode(date="1/13/99", number=3)

    # Guests
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")