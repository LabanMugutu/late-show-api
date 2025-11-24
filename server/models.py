from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# ============================================================
# EPISODE MODEL
# ============================================================

class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    # Prevent infinite recursion when serializing
    serialize_rules = ("-appearances.episode",)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # One episode has many appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Episode id={self.id}, date={self.date}, number={self.number}>"

# ============================================================
# GUEST MODEL
# ============================================================

class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    serialize_rules = ("-appearances.guest",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # One guest has many appearances
    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Guest id={self.id}, name={self.name}, occupation={self.occupation}>"

# ============================================================
# APPEARANCE MODEL
# ============================================================

class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    # Prevent recursion when serializing nested objects
    serialize_rules = ("-episode.appearances", "-guest.appearances")

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # Foreign Keys
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"))

    # Relationships
    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # -----------------------------------------
    # VALIDATION FOR RATING 1 TO 5
    # -----------------------------------------
    @validates("rating")
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value

    def __repr__(self):
        return (
            f"<Appearance id={self.id}, rating={self.rating}, "
            f"episode_id={self.episode_id}, guest_id={self.guest_id}>"
        )
