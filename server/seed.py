"""
Seed script to create initial data.

Run:
    python server/seed.py
This will create (or replace) `app.db` in project root.
"""
from app import create_app
from models import db, Episode, Guest, Appearance
