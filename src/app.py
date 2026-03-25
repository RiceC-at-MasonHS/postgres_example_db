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
    session = get_db()
    trainer = queries.get_trainer_by_id(session, trainer_id)
    if not trainer:
        return "Trainer not found", 404

    team = queries.get_trainer_team(session, trainer_id)
    return render_template('trainer_profile.html', trainer=trainer, team=team)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
