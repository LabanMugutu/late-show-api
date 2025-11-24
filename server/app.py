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
def create_app(test_config=None):
"""Application factory. If `test_config` is provided it's applied to app.config
(used by tests to use in-memory sqlite)."""
app = Flask(__name__, instance_relative_config=False)


# Default database (local file) - can be overridden through env var or tests
database_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Apply test config if provided
if test_config:
app.config.update(test_config)


# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


@app.route('/')
def index():
"""Basic index to verify server is running."""
return jsonify({'message': 'Welcome to the Late Show API!'}), 200