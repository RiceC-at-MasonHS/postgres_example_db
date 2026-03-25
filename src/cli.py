"""
CLI application for Pokedex Database Lab.
Interactive command-line tool for managing Pokemon, Trainers, and Collections.
"""

import click
from src.db import get_session, init_db
from src.models import Pokemon, Trainer, Collection
from src import queries


@click.group()
def cli():
    """Pokedex Database Lab - A teaching tool for database newcomers."""
    pass


# ============================================================================
# DATABASE MANAGEMENT COMMANDS
# ============================================================================

@cli.group()
def db():
    """Manage the database schema and data."""
    pass


@db.command()
def init():
    """Initialize the database schema."""
    click.echo("Initializing database...")
    init_db()


@db.command()
def seed():
    """Seed the database with initial Pokemon and a trainer."""
    session = get_session()

    # Starter Pokemon
    starters = [
        {"name": "Bulbasaur", "type1": "Grass", "type2": "Poison", "hp": 45, "attack": 49, "defense": 49, "speed": 45},
        {"name": "Charmander", "type1": "Fire", "type2": None, "hp": 39, "attack": 52, "defense": 43, "speed": 65},
        {"name": "Squirtle", "type1": "Water", "type2": None, "hp": 44, "attack": 48, "defense": 65, "speed": 43},
        {"name": "Pikachu", "type1": "Electric", "type2": None, "hp": 35, "attack": 55, "defense": 40, "speed": 90},
    ]

    for s in starters:
        if not queries.find_pokemon_by_name(session, s["name"]):
            new_p = Pokemon(**s)
            session.add(new_p)
            click.echo(f"Added {s['name']} to Pokedex.")

    # A classic Trainer
    if not queries.list_all_trainers(session):
        ash = Trainer(name="Ash Ketchum", hometown="Pallet Town")
        session.add(ash)
        click.echo("Added Ash Ketchum as a trainer.")
        session.commit()

        # Ash catches Pikachu
        pikachu = queries.find_pokemon_by_name(session, "Pikachu")
        if pikachu:
            queries.catch_pokemon(session, ash.id, pikachu.id, nickname="Buddy", level=5)
            click.echo("Ash caught Pikachu!")

    session.commit()
    click.echo(click.style("✓ Database seeded successfully!", fg="green"))
    session.close()


# ============================================================================
# POKEMON COMMANDS
# ============================================================================

@cli.group()
def pokemon():
    """Manage the Pokedex (Pokemon encyclopedia)."""
    pass


@pokemon.command(name="list")
def list_pokemon():
    """List all Pokemon in the Pokedex."""
    session = get_session()
    pokemon_list = queries.list_all_pokemon(session)

    if not pokemon_list:
        click.echo("No Pokemon found in the Pokedex.")
        session.close()
        return

    click.echo(f"\n{'ID':<5} {'Name':<15} {'Type 1':<10} {'Type 2':<10} {'HP':<5} {'ATK':<5} {'DEF':<5}")
    click.echo("-" * 65)
    for p in pokemon_list:
        click.echo(f"{p.id:<5} {p.name:<15} {p.type1:<10} {p.type2 or '-':<10} {p.hp:<5} {p.attack:<5} {p.defense:<5}")
    click.echo(f"\nTotal: {len(pokemon_list)} Pokemon\n")
    session.close()


@pokemon.command()
def add():
    """Add a new Pokemon to the Pokedex (interactive)."""
    session = get_session()

    name = click.prompt("Pokemon Name").title().strip()
    type1 = click.prompt("Primary Type").title().strip()
    type2 = click.prompt("Secondary Type (optional, press Enter to skip)", default="").title().strip()
    hp = click.prompt("HP", type=int, default=50)
    attack = click.prompt("Attack", type=int, default=50)
    defense = click.prompt("Defense", type=int, default=50)
    speed = click.prompt("Speed", type=int, default=50)

    # Check for duplicate
    existing = queries.find_pokemon_by_name(session, name)
    if existing:
        click.echo(click.style(f"✗ {name} already exists in the Pokedex!", fg="red"))
        session.close()
        return

    # Create Pokemon
    new_pokemon = Pokemon(
        name=name,
        type1=type1,
        type2=type2 if type2 else None,
        hp=hp,
        attack=attack,
        defense=defense,
        speed=speed
    )
    session.add(new_pokemon)
    session.commit()

    click.echo(click.style(f"✓ {name} added to Pokedex (ID: {new_pokemon.id})", fg="green"))
    session.close()


# ============================================================================
# TRAINER COMMANDS
# ============================================================================

@cli.group()
def trainer():
    """Manage Pokemon trainers."""
    pass


@trainer.command(name="list")
def list_trainers():
    """List all trainers."""
    session = get_session()
    trainers = queries.list_all_trainers(session)

    if not trainers:
        click.echo("No trainers found.")
        session.close()
        return

    click.echo(f"\n{'ID':<5} {'Name':<20} {'Hometown':<20}")
    click.echo("-" * 50)
    for t in trainers:
        click.echo(f"{t.id:<5} {t.name:<20} {t.hometown or '-':<20}")
    click.echo(f"\nTotal: {len(trainers)} trainers\n")
    session.close()


@trainer.command()
def add():
    """Add a new trainer (interactive)."""
    session = get_session()

    name = click.prompt("Trainer Name")
    hometown = click.prompt("Hometown (optional, press Enter to skip)", default="")

    new_trainer = Trainer(name=name, hometown=hometown if hometown else None)
    session.add(new_trainer)
    session.commit()

    click.echo(click.style(f"✓ Trainer {name} registered! (ID: {new_trainer.id})", fg="green"))
    session.close()


@cli.command()
@click.argument("trainer_id", type=int)
@click.argument("pokemon_id", type=int)
@click.option("--nickname", default=None, help="Nickname for the Pokemon")
@click.option("--level", default=1, type=int, help="Starting level")
def catch(trainer_id: int, pokemon_id: int, nickname: str, level: int):
    """Assign a Pokemon to a trainer's collection."""
    session = get_session()

    trainer = queries.get_trainer_by_id(session, trainer_id)
    pokemon = queries.get_pokemon_by_id(session, pokemon_id)

    if not trainer:
        click.echo(click.style("✗ Trainer not found!", fg="red"))
        session.close()
        return
    if not pokemon:
        click.echo(click.style("✗ Pokemon species not found!", fg="red"))
        session.close()
        return

    catch_record = queries.catch_pokemon(session, trainer_id, pokemon_id, nickname, level)
    click.echo(click.style(f"✓ {trainer.name} caught a {pokemon.name}!", fg="green"))
    if nickname:
        click.echo(f"  Nickname: '{nickname}'")
    click.echo(f"  Level: {level}")
    session.close()


@trainer.command()
@click.argument("trainer_id", type=int)
def team(trainer_id: int):
    """View a trainer's current collection of Pokemon."""
    session = get_session()
    trainer = queries.get_trainer_by_id(session, trainer_id)

    if not trainer:
        click.echo(click.style("✗ Trainer not found!", fg="red"))
        session.close()
        return

    team_members = queries.get_trainer_team(session, trainer_id)

    click.echo(f"\n{'='*60}")
    click.echo(f"Team for {trainer.name} (from {trainer.hometown or 'Unknown'})")
    click.echo(f"{'='*60}")

    if not team_members:
        click.echo("(No Pokemon caught yet)")
    else:
        click.echo(f"{'Species':<15} {'Nickname':<15} {'Level':<5} {'Types':<20}")
        click.echo("-" * 60)
        for m in team_members:
            p = m.pokemon
            types = f"{p.type1}{'/' + p.type2 if p.type2 else ''}"
            click.echo(f"{p.name:<15} {m.nickname or '-':<15} {m.level:<5} {types:<20}")

    click.echo(f"{'='*60}\n")
    session.close()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    cli()
