"""
SQLAlchemy ORM models for Pokedex Database Lab.
Defines Pokemon, Trainer, and Collection entities.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Pokemon(Base):
    """
    An entry in the Pokedex.
    Represents the species-level data for a Pokemon.
    """
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    type1 = Column(String(50), nullable=False)
    type2 = Column(String(50), nullable=True)
    hp = Column(Integer, default=50)
    attack = Column(Integer, default=50)
    defense = Column(Integer, default=50)
    speed = Column(Integer, default=50)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship to collections (which trainers have this species)
    collections = relationship("Collection", back_populates="pokemon", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pokemon(id={self.id}, name='{self.name}', type='{self.type1}')>"


class Trainer(Base):
    """
    A Pokemon Trainer.
    """
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hometown = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship to the trainer's collection of Pokemon
    collection = relationship("Collection", back_populates="trainer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trainer(id={self.id}, name='{self.name}')>"


class Collection(Base):
    """
    A specific Pokemon instance caught by a trainer.
    This is a join table between Trainer and Pokemon with extra attributes.
    """
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id", ondelete="CASCADE"), nullable=False)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"), nullable=False)
    nickname = Column(String(100), nullable=True)
    level = Column(Integer, default=1)
    caught_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    trainer = relationship("Trainer", back_populates="collection")
    pokemon = relationship("Pokemon", back_populates="collections")

    def __repr__(self):
        return f"<Collection(trainer='{self.trainer.name}', pokemon='{self.pokemon.name}', nickname='{self.nickname}')>"
