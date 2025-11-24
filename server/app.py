"""
Main Flask application (Controller). Runs on port 5555 when executed directly.

Endpoints implemented:
- GET /episodes
- GET /episodes/<int:id>
- DELETE /episodes/<int:id>
- GET /guests
- POST /appearances

This file performs explicit JSON shaping so responses match the challenge spec.
"""
import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
from models import db, Episode, Guest, Appearance

def create_app(test_config=None):
    """Factory to create Flask app. test_config overrides default config when provided."""
    app = Flask(__name__, instance_relative_config=False)

    # Default DB (file) - override with DATABASE_URL env var or test config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)
    api = Api(app)

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Late Show API!"}), 200

    # --------------------
    # Helper serializers
    # --------------------
    def episode_simple_dict(ep: Episode):
        """Return {id, date, number}"""
        return {"id": ep.id, "date": ep.date, "number": ep.number}

    def guest_simple_dict(g: Guest):
        """Return {id, name, occupation}"""
        return {"id": g.id, "name": g.name, "occupation": g.occupation}

    def appearance_dict_for_episode(a: Appearance):
        """
        Return appearance shaped for GET /episodes/<id> as in spec:
        {
          "episode_id": 1,
          "guest": {...},
          "guest_id": 1,
          "id": 1,
          "rating": 4
        }
        """
        return {
            "episode_id": a.episode_id,
            "guest": guest_simple_dict(a.guest),
            "guest_id": a.guest_id,
            "id": a.id,
            "rating": a.rating
        }

    def appearance_full_response(a: Appearance):
        """
        Return appearance shaped for POST /appearances response:
        {
          "id": 162,
          "rating": 5,
          "guest_id": 3,
          "episode_id": 2,
          "episode": {id,date,number},
          "guest": {id,name,occupation}
        }
        """
        return {
            "id": a.id,
            "rating": a.rating,
            "guest_id": a.guest_id,
            "episode_id": a.episode_id,
            "episode": episode_simple_dict(a.episode),
            "guest": guest_simple_dict(a.guest)
        }

    # --------------------
    # Resource classes
    # --------------------
    class EpisodesListResource(Resource):
        def get(self):
            eps = Episode.query.order_by(Episode.id).all()
            return [episode_simple_dict(e) for e in eps], 200

    class EpisodeResource(Resource):
        def get(self, id):
            ep = Episode.query.get(id)
            if not ep:
                return {"error": "Episode not found"}, 404
            # include appearances with nested guest info
            resp = {
                "id": ep.id,
                "date": ep.date,
                "number": ep.number,
                "appearances": [appearance_dict_for_episode(a) for a in ep.appearances]
            }
            return resp, 200

        def delete(self, id):
            ep = Episode.query.get(id)
            if not ep:
                return {"error": "Episode not found"}, 404
            db.session.delete(ep)
            db.session.commit()
            # 204 No Content must return empty body
            return "", 204

    class GuestsListResource(Resource):
        def get(self):
            gs = Guest.query.order_by(Guest.id).all()
            return [guest_simple_dict(g) for g in gs], 200

    class AppearancesResource(Resource):
        def post(self):
            data = request.get_json() or {}
            rating = data.get("rating")
            episode_id = data.get("episode_id")
            guest_id = data.get("guest_id")

            errors = []
            if rating is None:
                errors.append("rating is required")
            if episode_id is None:
                errors.append("episode_id is required")
            if guest_id is None:
                errors.append("guest_id is required")
            if errors:
                return {"errors": errors}, 400

            # verify related objects
            episode = Episode.query.get(episode_id)
            guest = Guest.query.get(guest_id)
            if not episode:
                return {"errors": [f"Episode with id {episode_id} not found"]}, 400
            if not guest:
                return {"errors": [f"Guest with id {guest_id} not found"]}, 400

            # create appearance; model validators will enforce rating constraints
            try:
                # Ensure integer rating
                rating_int = int(rating)
                appearance = Appearance(rating=rating_int, episode=episode, guest=guest)
                db.session.add(appearance)
                db.session.commit()
            except ValueError as ve:
                db.session.rollback()
                return {"errors": [str(ve)]}, 400
            except IntegrityError as ie:
                db.session.rollback()
                return {"errors": [str(ie.orig)]}, 400
            except Exception as e:
                db.session.rollback()
                return {"errors": [str(e)]}, 400

            return appearance_full_response(appearance), 201

    # --------------------
    # Route registration
    # --------------------
    api.add_resource(EpisodesListResource, "/episodes")
    api.add_resource(EpisodeResource, "/episodes/<int:id>")
    api.add_resource(GuestsListResource, "/guests")
    api.add_resource(AppearancesResource, "/appearances")

    return app

if __name__ == "__main__":
    # run on port 5555 as required by challenge
    app = create_app()
    app.run(port=5555, debug=True)

