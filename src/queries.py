"""
Database query logic for Pokedex Database Lab.
Handles CRUD operations for Pokemon and Trainers.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.models import Pokemon, Trainer, Collection

# ============================================================================
# POKEMON QUERIES
# ============================================================================

def list_all_pokemon(session: Session) -> List[Pokemon]:
    """List all Pokemon in the Pokedex."""
    return session.query(Pokemon).order_by(Pokemon.id).all()

def get_pokemon_by_id(session: Session, pokemon_id: int) -> Optional[Pokemon]:
    """Retrieve a specific Pokemon by ID."""
    return session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

def find_pokemon_by_name(session: Session, name: str) -> Optional[Pokemon]:
    """Find a Pokemon by its name (exact match)."""
    return session.query(Pokemon).filter(Pokemon.name.ilike(name)).first()

def search_pokemon(session: Session, query: str) -> List[Pokemon]:
    """Search Pokemon by name or types."""
    return session.query(Pokemon).filter(
        (Pokemon.name.ilike(f"%{query}%")) |
        (Pokemon.type1.ilike(f"%{query}%")) |
        (Pokemon.type2.ilike(f"%{query}%"))
    ).all()

# ============================================================================
# TRAINER QUERIES
# ============================================================================

def list_all_trainers(session: Session) -> List[Trainer]:
    """List all trainers."""
    return session.query(Trainer).order_by(Trainer.id).all()

def get_trainer_by_id(session: Session, trainer_id: int) -> Optional[Trainer]:
    """Retrieve a specific trainer by ID."""
    return session.query(Trainer).filter(Trainer.id == trainer_id).first()

def get_trainer_team(session: Session, trainer_id: int) -> List[Collection]:
    """List a trainer's current collection of caught Pokemon."""
    return session.query(Collection).filter(Collection.trainer_id == trainer_id).all()

# ============================================================================
# COLLECTION QUERIES
# ============================================================================

def catch_pokemon(session: Session, trainer_id: int, pokemon_id: int, nickname: str = None, level: int = 1) -> Collection:
    """Assign a Pokemon to a trainer (the 'Catch' mechanic)."""
    new_catch = Collection(
        trainer_id=trainer_id,
        pokemon_id=pokemon_id,
        nickname=nickname,
        level=level
    )
    session.add(new_catch)
    session.commit()
    return new_catch

def update_collection_level(session: Session, collection_id: int, new_level: int) -> Optional[Collection]:
    """Update the level of a caught Pokemon."""
    record = session.query(Collection).filter(Collection.id == collection_id).first()
    if record:
        record.level = new_level
        session.commit()
    return record

def delete_collection_record(session: Session, collection_id: int) -> bool:
    """Remove a Pokemon from a trainer's collection (the 'Release' mechanic)."""
    record = session.query(Collection).filter(Collection.id == collection_id).first()
    if record:
        session.delete(record)
        session.commit()
        return True
    return False
