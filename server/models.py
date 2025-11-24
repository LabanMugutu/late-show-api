"""
Database models for the Late Show API. Contains Episode, Guest, and Appearance.
Models include explicit `to_dict()` methods crafted to match the expected JSON
formats described in the challenge. Validations ensure data integrity.
"""


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates