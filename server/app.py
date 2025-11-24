"""
Main Flask application (Controller). Exposes the API endpoints required by the
challenge. Uses Flask-RESTful Resource classes for clear separation of route
handlers.


Run with:
python server/app.py


The app uses a factory `create_app()` so tests can supply a test config.
"""


from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance
from sqlalchemy.exc import IntegrityError
import os