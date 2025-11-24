"""
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


# Verify foreign objects exist
episode = Episode.query.get(episode_id)
guest = Guest.query.get(guest_id)
if not episode:
return {'errors': [f'Episode with id {episode_id} not found']}, 400
if not guest:
return {'errors': [f'Guest with id {guest_id} not found']}, 400


# Create appearance and rely on model validation to enforce rating range
try:
appearance = Appearance(rating=int(rating), episode=episode, guest=guest)
db.session.add(appearance)
db.session.commit()
except ValueError as ve:
db.session.rollback()
return {'errors': [str(ve)]}, 400
except (IntegrityError, Exception) as e:
db.session.rollback()
return {'errors': [str(e)]}, 400


# Return appearance with nested episode and guest (shaped to spec)
return appearance.to_dict(include_episode=True, include_guest=True), 201


# Register resources with their routes
api.add_resource(EpisodesListResource, '/episodes')
api.add_resource(EpisodeResource, '/episodes/<int:id>')
api.add_resource(GuestsListResource, '/guests')
api.add_resource(AppearancesResource, '/appearances')


return app




if __name__ == '__main__':
# When running directly, create app and run on port 5555 for the challenge
app = create_app()
app.run(port=5555, debug=True)
