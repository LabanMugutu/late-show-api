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
# ------------------ Resource classes ------------------
If not found return 404; on success return 204 No Content with empty body.
"""
ep = Episode.query.get(id)
if not ep:
return {'error': 'Episode not found'}, 404
db.session.delete(ep)
db.session.commit()
return '', 204


class GuestsListResource(Resource):
def get(self):
"""GET /guests - return array of guest objects (id, name, occupation)"""
guests = Guest.query.order_by(Guest.id).all()
return [g.to_dict(simple=True) for g in guests], 200


class AppearancesResource(Resource):
def post(self):
"""POST /appearances - create a new appearance.


Expected JSON:
{
"rating": 5,
"episode_id": 2,
"guest_id": 3
}


Success: 201 with appearance including nested episode and guest as in spec.
Validation errors: 400 with {"errors": [ ... ]}
"""
data = request.get_json() or {}
rating = data.get('rating')
episode_id = data.get('episode_id')
guest_id = data.get('guest_id')


errors = []
# Basic presence checks
if rating is None:
errors.append('rating is required')
if episode_id is None:
errors.append('episode_id is required')
if guest_id is None:
errors.append('guest_id is required')


if errors:
return {'errors': errors}, 400
