"""
Tests for Pokedex Database Lab.
Verifies Pokemon CRUD operations and database constraints.
"""

import pytest
from src.db import get_session, init_db
from src.models import Base, Pokemon, Trainer, Collection
from src import queries

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Initializes the test database schema."""
    init_db()
    yield

@pytest.fixture
def session():
    """Provides a clean database session for each test."""
    session = get_session()
    # Clean tables before each test
    session.query(Collection).delete()
    session.query(Trainer).delete()
    session.query(Pokemon).delete()
    session.commit()
    yield session
    session.close()

def test_add_pokemon(session):
    """Test that a Pokemon can be added to the Pokedex."""
    new_p = Pokemon(name="Charmander", type1="Fire", hp=39, attack=52, defense=43)
    session.add(new_p)
    session.commit()

    saved_p = queries.find_pokemon_by_name(session, "Charmander")
    assert saved_p is not None
    assert saved_p.name == "Charmander"
    assert saved_p.type1 == "Fire"

def test_trainer_registration(session):
    """Test that a trainer can be registered."""
    ash = Trainer(name="Ash Ketchum", hometown="Pallet Town")
    session.add(ash)
    session.commit()

    saved_t = session.query(Trainer).filter(Trainer.name == "Ash Ketchum").first()
    assert saved_t is not None
    assert saved_t.hometown == "Pallet Town"

def test_catch_mechanic(session):
    """Test that a trainer can catch a Pokemon."""
    # Setup: Add a Pokemon and a Trainer
    p = Pokemon(name="Pikachu", type1="Electric")
    t = Trainer(name="Red")
    session.add_all([p, t])
    session.commit()

    # Act: Catch the Pokemon
    queries.catch_pokemon(session, t.id, p.id, nickname="Sparky", level=5)

    # Assert: Verify the team
    team = queries.get_trainer_team(session, t.id)
    assert len(team) == 1
    assert team[0].nickname == "Sparky"
    assert team[0].pokemon.name == "Pikachu"

# ============================================================================
# BUG REPRODUCTION (TDD ASSIGNMENT)
# ============================================================================

def test_pokemon_attack_should_be_positive(session):
    """
    FAILURE TEST: Currently, our database allows negative attack points!
    This test is EXPECTED TO FAIL until students fix it.
    """
    negative_p = Pokemon(name="Glitch", type1="Ghost", attack=-10)
    session.add(negative_p)
    session.commit()

    # If the database allows this, it is technically a bug in our game rules.
    # We want this test to fail when a negative attack value is provided.
    assert negative_p.attack >= 0, f"Pokemon {negative_p.name} has negative attack: {negative_p.attack}!"
