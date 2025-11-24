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
# One-to-many: Episode -> Appearance
appearances = db.relationship(
'Appearance', back_populates='episode', cascade='all, delete-orphan'
)


def __repr__(self):
return f"<Episode {self.id} #{self.number} {self.date}>"


def to_dict(self, simple=False):
"""Return a dictionary matching the API spec.


If simple=True returns: {id, date, number}
If simple=False returns full episode with appearances nested.
"""
base = {'id': self.id, 'date': self.date, 'number': self.number}
if simple:
return base
# full representation includes appearances (each appearance shaped per spec)
base['appearances'] = [a.to_dict(include_guest=True, include_episode=False) for a in self.appearances]
return base

class Guest(db.Model):
"""Guest model: id, name, occupation


Relationships:
- appearances: list of Appearance objects
"""


__tablename__ = 'guests'


id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String, nullable=False)
occupation = db.Column(db.String, nullable=True)