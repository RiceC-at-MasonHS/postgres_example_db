from flask import Flask, render_template, request, redirect, url_for, g
from src.db import get_session
from src.models import Pokemon, Trainer, Collection
from src import queries
import os

# Calculate the path to the root templates folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

def get_db():
    if 'db' not in g:
        g.db = get_session()
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    """Display the full Pokedex."""
    session = get_db()
    pokemon_list = queries.list_all_pokemon(session)
    return render_template('index.html', pokemon_list=pokemon_list)

@app.route('/trainers')
def trainers():
    """Display all trainers."""
    session = get_db()
    trainers_list = queries.list_all_trainers(session)
    return render_template('trainers.html', trainers=trainers_list)

@app.route('/trainer/<int:trainer_id>')
def trainer_profile(trainer_id):
    """View a specific trainer and their team."""
    from sqlalchemy import text
    session = get_db()
    trainer = queries.get_trainer_by_id(session, trainer_id)
    if not trainer:
        return "Trainer not found", 404

    # Fetch team with optional columns added during migrations
    # We use raw SQL to ensure we get any columns added after the app started
    team_query = text("""
        SELECT c.*, p.name as species_name, p.type1, p.hp, p.attack, p.defense
        FROM collections c
        JOIN pokemon p ON c.pokemon_id = p.id
        WHERE c.trainer_id = :trainer_id
    """)
    team_rows = session.execute(team_query, {"trainer_id": trainer_id}).fetchall()
    
    # Convert to a list of dicts for easy template access
    team = []
    for row in team_rows:
        team.append(row._asdict())

    return render_template('trainer_profile.html', trainer=trainer, team=team)

@app.route('/collection/level-up/<int:collection_id>', methods=['POST'])
def level_up(collection_id):
    """Increase a Pokemon's level by 1."""
    session = get_db()
    record = session.query(Collection).filter(Collection.id == collection_id).first()
    if record:
        queries.update_collection_level(session, collection_id, record.level + 1)
    return redirect(url_for('trainer_profile', trainer_id=record.trainer_id))

@app.route('/collection/release/<int:collection_id>', methods=['POST'])
def release_pokemon(collection_id):
    """Release a Pokemon from a trainer's collection."""
    session = get_db()
    record = session.query(Collection).filter(Collection.id == collection_id).first()
    if record:
        trainer_id = record.trainer_id
        queries.delete_collection_record(session, collection_id)
        return redirect(url_for('trainer_profile', trainer_id=trainer_id))
    return redirect(url_for('trainers'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
