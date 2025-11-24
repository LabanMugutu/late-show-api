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

    db.session.add_all([e1, e2, e3, g1, g2, g3])
    db.session.commit()

    # Appearances
    a1 = Appearance(rating=4, episode=e1, guest=g1)
    a2 = Appearance(rating=5, episode=e2, guest=g3)
    a3 = Appearance(rating=3, episode=e1, guest=g2)

    db.session.add_all([a1, a2, a3])
    db.session.commit()

    print("Seeded database successfully.")
