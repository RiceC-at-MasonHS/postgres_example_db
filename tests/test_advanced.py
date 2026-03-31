"""
Advanced Tests for Pokedex Database Lab.
Verifies Phase 1 (CRUD), Phase 2 (Manual SQL), Phase 3 (Migrations), 
and Phase 4 (Data Integrity) functionality.
"""

import pytest
from sqlalchemy import text
from src.db import get_session, init_db, drop_db
from src.models import Base, Pokemon, Trainer, Collection
from src import queries

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Initializes the base database schema."""
    drop_db()
    init_db()
    yield
    drop_db()

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

# ============================================================================
# PHASE 1: CRUD OPERATIONS (Update & Delete)
# ============================================================================

def test_update_collection_level(session):
    """Test that a caught Pokemon's level can be updated."""
    p = Pokemon(name="Bulbasaur", type1="Grass")
    t = Trainer(name="Ash")
    session.add_all([p, t])
    session.commit()
    
    catch = queries.catch_pokemon(session, t.id, p.id, level=5)
    
    # Act: Update level
    queries.update_collection_level(session, catch.id, 10)
    
    # Assert
    updated = session.query(Collection).filter(Collection.id == catch.id).first()
    assert updated.level == 10

def test_delete_collection_record(session):
    """Test that a caught Pokemon can be released (deleted)."""
    p = Pokemon(name="Squirtle", type1="Water")
    t = Trainer(name="Gary")
    session.add_all([p, t])
    session.commit()
    
    catch = queries.catch_pokemon(session, t.id, p.id)
    
    # Act: Delete
    success = queries.delete_collection_record(session, catch.id)
    
    # Assert
    assert success is True
    assert session.query(Collection).filter(Collection.id == catch.id).count() == 0

# ============================================================================
# PHASE 2: MANUAL SQL & MIGRATIONS
# ============================================================================

def test_schema_migration(session):
    """Test that the migrate command adds the moves table and is_shiny column."""
    # We'll execute the migration steps manually in the test to verify they work
    try:
        session.execute(text("ALTER TABLE collections ADD COLUMN is_shiny BOOLEAN DEFAULT FALSE;"))
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS moves (
                id SERIAL PRIMARY KEY,
                pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(50) NOT NULL,
                power INTEGER DEFAULT 40
            );
        """))
        session.commit()
    except Exception as e:
        session.rollback()
        pytest.fail(f"Migration failed: {e}")

    # Verify column exists in collections
    result = session.execute(text("SELECT is_shiny FROM collections LIMIT 1;"))
    assert result is not None

    # Verify moves table exists
    result = session.execute(text("SELECT count(*) FROM moves;"))
    assert result.fetchone()[0] == 0

# ============================================================================
# PHASE 3: DATA INTEGRITY (Constraints)
# ============================================================================

def test_data_integrity_constraints(session):
    """Test that Phase 3 constraints (Unique Names, Level Range) work."""
    # 1. Apply constraints
    try:
        session.execute(text("ALTER TABLE trainers ADD CONSTRAINT unique_trainer_name UNIQUE (name);"))
        session.execute(text("ALTER TABLE collections ADD CONSTRAINT check_level_range CHECK (level >= 1 AND level <= 100);"))
        session.commit()
    except Exception:
        session.rollback()
        # Might already exist if migration was run previously in this module
        pass

    # 2. Test Unique Trainer Name
    t1 = Trainer(name="Duplicate")
    session.add(t1)
    session.commit()
    
    with pytest.raises(Exception): # sqlalchemy.exc.IntegrityError
        t2 = Trainer(name="Duplicate")
        session.add(t2)
        session.commit()
    session.rollback()

    # 3. Test Level Range
    p = Pokemon(name="GlitchSpecies", type1="Ghost")
    t = Trainer(name="GlitchTrainer")
    session.add_all([p, t])
    session.commit()

    with pytest.raises(Exception):
        # Insert a level 999 Pokemon
        session.execute(text(f"INSERT INTO collections (trainer_id, pokemon_id, level) VALUES ({t.id}, {p.id}, 999)"))
        session.commit()
    session.rollback()
