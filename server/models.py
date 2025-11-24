"""
Database models for the Late Show API. Contains Episode, Guest, and Appearance.
Models include explicit `to_dict()` methods crafted to match the expected JSON
formats described in the challenge. Validations ensure data integrity.
"""


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
# Initialize SQLAlchemy - the app will call db.init_app(app)
db = SQLAlchemy()

class Episode(db.Model):
"""Episode model: id, date (string), number (int)


Relationships:
- appearances: list of Appearance objects


to_dict(simple=True) returns the reduced shape used by GET /episodes.
to_dict(simple=False) returns the full shape used by GET /episodes/<id>.
"""


__tablename__ = 'episodes'


id = db.Column(db.Integer, primary_key=True)
date = db.Column(db.String, nullable=False)
number = db.Column(db.Integer, nullable=False)