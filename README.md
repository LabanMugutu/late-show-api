# Late Show API (Flask)

Complete implementation for the Weekend Flask challenge. The project exposes a RESTful API to manage Episodes, Guests, and Appearances.

## Quickstart

1. Create virtual env and activate:

```bash
python3 -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Seed the database (creates app.db):

bash
Copy code
python server/seed.py
Run server:

bash
Copy code
python server/app.py
Visit: http://localhost:5555

Endpoints
GET /episodes — list of episodes [ {id, date, number}, ... ].

GET /episodes/<id> — episode with nested appearances & guest info.

DELETE /episodes/<id> — deletes episode (and its appearances). Returns 204.

GET /guests — list of guests [ {id, name, occupation}, ... ].

POST /appearances — create appearance; accepts {rating, episode_id, guest_id}.

Testing
Run the test suite (uses in-memory SQLite):

bash
Copy code
pytest -x
Notes
Appearance rating is validated to be an integer between 1 and 5.

Deleting an Episode (or Guest) cascades to delete its Appearance rows (no orphans).

Responses are intentionally shaped to match the challenge example JSON.

---

## Final checklist & notes
- These files match the expectations in the rubric (models + relationships + validations + routes + response shapes + tests).  
- `server/models.py` you previously confirmed must remain in the project and is compatible with this `app.py` because `app.py` explicitly shapes responses using model attributes, not relying on `to_dict()` specifics.
- After pasting the files, run:
  1. `python -m venv env && source env/bin/activate`
  2. `pip install -r requirements.txt`
  3. `python server/seed.py`
  4. `python server/app.py`
  5. In another terminal run `pytest -x` to run tests.

Author Laban Mugutu