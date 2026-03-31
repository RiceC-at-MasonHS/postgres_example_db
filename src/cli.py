"""
CLI application for Pokedex Database Lab.
Interactive command-line tool for managing Pokemon, Trainers, and Collections.
"""

import click
from src.db import get_session, init_db, drop_db
from src.models import Pokemon, Trainer, Collection
from src import queries


@click.group()
def cli():
    """Pokedex Database Lab - A teaching tool for database newcomers."""
    pass


# ============================================================================
# PHASE 1: DATABASE MANAGEMENT COMMANDS
# ============================================================================

@cli.group()
def db():
    """Manage the database schema and data."""
    pass


@db.command()
@click.option("--on/--off", default=True, help="Turn SQL logging on or off.")
def logs(on):
    """Toggle the detailed SQL logs (useful for learning or debugging)."""
    import os
    quiet_file = ".quiet_sql"
    
    if on:
        if os.path.exists(quiet_file):
            os.remove(quiet_file)
        click.echo(click.style("✓ SQL Logging enabled! (Detailed database output is ON)", fg="green"))
    else:
        with open(quiet_file, "w") as f:
            f.write("quiet")
        click.echo(click.style("✓ SQL Logging disabled! (Detailed database output is OFF)", fg="yellow"))
    
    click.echo("Tip: Run 'pokemon list' to see the difference.")


@db.command()
def init():
    """Initialize the base database schema."""
    click.echo("Initializing database...")
    init_db()


@db.command()
def reset():
    """Drop and recreate all database tables (HARD RESET)."""
    if click.confirm("Are you sure you want to delete ALL data and reset the database?"):
        click.echo("Dropping tables...")
        drop_db()
        click.echo("Recreating tables...")
        init_db()
        click.echo(click.style("✓ Database reset complete!", fg="green"))


@db.command()
def seed():
    """Seed the database with Gen 1 starters and Ash."""
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
    click.echo(click.style("✓ Gen 1 (Kanto) data seeded!", fg="green"))
    session.close()


@db.command()
def seed2():
    """Seed the database with Gen 2 starters and Misty."""
    session = get_session()

    johto = [
        {"name": "Chikorita", "type1": "Grass", "type2": None, "hp": 45, "attack": 49, "defense": 65, "speed": 45},
        {"name": "Cyndaquil", "type1": "Fire", "type2": None, "hp": 39, "attack": 52, "defense": 43, "speed": 65},
        {"name": "Totodile", "type1": "Water", "type2": None, "hp": 50, "attack": 65, "defense": 64, "speed": 43},
        {"name": "Marill", "type1": "Water", "type2": "Fairy", "hp": 70, "attack": 20, "defense": 50, "speed": 40},
    ]

    for p in johto:
        if not queries.find_pokemon_by_name(session, p["name"]):
            session.add(Pokemon(**p))
            click.echo(f"Added {p['name']} to Pokedex.")

    # Misty
    misty = session.query(Trainer).filter(Trainer.name == "Misty").first()
    if not misty:
        misty = Trainer(name="Misty", hometown="Cerulean City")
        session.add(misty)
        click.echo("Added Misty as a trainer.")
        session.commit()

        # Misty catches Marill
        marill = queries.find_pokemon_by_name(session, "Marill")
        if marill:
            queries.catch_pokemon(session, misty.id, marill.id, level=10)
            click.echo("Misty caught Marill!")

    session.commit()
    click.echo(click.style("✓ Gen 2 (Johto) data seeded!", fg="green"))
    session.close()


@db.command()
def seed3():
    """Seed the database with Gen 3 starters and Brock."""
    session = get_session()

    hoenn = [
        {"name": "Treecko", "type1": "Grass", "type2": None, "hp": 40, "attack": 45, "defense": 35, "speed": 70},
        {"name": "Torchic", "type1": "Fire", "type2": None, "hp": 45, "attack": 60, "defense": 40, "speed": 45},
        {"name": "Mudkip", "type1": "Water", "type2": None, "hp": 50, "attack": 70, "defense": 50, "speed": 40},
        {"name": "Geodude", "type1": "Rock", "type2": "Ground", "hp": 40, "attack": 80, "defense": 100, "speed": 20},
    ]

    for p in hoenn:
        if not queries.find_pokemon_by_name(session, p["name"]):
            session.add(Pokemon(**p))
            click.echo(f"Added {p['name']} to Pokedex.")

    # Brock
    brock = session.query(Trainer).filter(Trainer.name == "Brock").first()
    if not brock:
        brock = Trainer(name="Brock", hometown="Pewter City")
        session.add(brock)
        click.echo("Added Brock as a trainer.")
        session.commit()

        # Brock catches Geodude
        geodude = queries.find_pokemon_by_name(session, "Geodude")
        if geodude:
            queries.catch_pokemon(session, brock.id, geodude.id, level=12)
            click.echo("Brock caught Geodude!")

    session.commit()
    click.echo(click.style("✓ Gen 3 (Hoenn) data seeded!", fg="green"))
    session.close()



# ============================================================================
# PHASE 2: SCHEMA EVOLUTION (MIGRATIONS)
# ============================================================================

@db.command()
def migrate():
    """[ADV: Phase 3] Add moves table and is_shiny column to collections table."""
    from sqlalchemy import text
    session = get_session()
    
    click.echo("Executing Advanced Phase 3 Migration...")
    
    try:
        # Add is_shiny to collections table
        session.execute(text("ALTER TABLE collections ADD COLUMN is_shiny BOOLEAN DEFAULT FALSE;"))
        click.echo("✓ Added 'is_shiny' column to collections table.")

        # Create moves table
        session.execute(text("""
            CREATE TABLE moves (
                id SERIAL PRIMARY KEY,
                pokemon_id INTEGER REFERENCES pokemon(id) ON DELETE CASCADE,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(50) NOT NULL,
                power INTEGER DEFAULT 40
            );
        """))
        click.echo("✓ Created 'moves' table.")
        
        session.commit()
        click.echo(click.style("✓ Advanced Phase 3 Migration successful!", fg="green"))
    except Exception as e:
        session.rollback()
        click.echo(click.style(f"✗ Migration failed: {str(e)}", fg="red"))
    finally:
        session.close()


# ============================================================================
# PHASE 3: DATA INTEGRITY (CONSTRAINTS)
# ============================================================================

@db.command()
def secure():
    """[ADV: Phase 4] Add database-level constraints for data integrity."""
    from sqlalchemy import text
    session = get_session()
    
    click.echo("Executing Advanced Phase 4 Security Hardening...")
    
    try:
        # 1. Unique name for Trainers
        session.execute(text("ALTER TABLE trainers ADD CONSTRAINT unique_trainer_name UNIQUE (name);"))
        click.echo("✓ Added UNIQUE constraint to trainer names.")

        # 2. Level range for Collections (must be 1-100)
        # Note: Postgres syntax for adding check constraint
        session.execute(text("ALTER TABLE collections ADD CONSTRAINT check_level_range CHECK (level >= 1 AND level <= 100);"))
        click.echo("✓ Added CHECK constraint to pokemon levels (1-100).")
        
        session.commit()
        click.echo(click.style("✓ Advanced Phase 4 Security complete!", fg="green"))
    except Exception as e:
        session.rollback()
        click.echo(click.style(f"✗ Security hardening failed: {str(e)}", fg="red"))
    finally:
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

    click.echo(f"\n{'='*80}")
    click.echo(f"Team for {trainer.name} (from {trainer.hometown or 'Unknown'})")
    click.echo(f"{'='*80}")

    if not team_members:
        click.echo("(No Pokemon caught yet)")
    else:
        click.echo(f"{'Collection ID':<15} {'Species':<12} {'Nickname':<12} {'LVL':<5} {'HP':<4} {'ATK':<4} {'DEF':<4} {'Types':<15}")
        click.echo("-" * 80)
        for m in team_members:
            p = m.pokemon
            types = f"{p.type1}{'/' + p.type2 if p.type2 else ''}"

            # Simple 5% stat boost per level: Base * (1 + (Level-1) * 0.05)
            multiplier = 1 + (m.level - 1) * 0.05
            hp = int(p.hp * multiplier)
            atk = int(p.attack * multiplier)
            dfe = int(p.defense * multiplier)

            click.echo(f"{m.id:<15} {p.name:<12} {m.nickname or '-':<12} {m.level:<5} {hp:<4} {atk:<4} {dfe:<4} {types:<15}")


    click.echo(f"{'='*80}\n")
    session.close()


@trainer.command(name="shiny")
@click.argument("collection_id", type=int)
@click.option("--on/--off", default=True, help="Set the shiny status.")
def toggle_shiny(collection_id: int, on: bool):
    """Toggle the 'Shiny' status of a caught Pokemon."""
    from sqlalchemy import text
    session = get_session()
    
    try:
        status = "TRUE" if on else "FALSE"
        # We use raw SQL here because the ORM model doesn't know about 'is_shiny' yet!
        session.execute(text(f"UPDATE collections SET is_shiny = {status} WHERE id = :id"), {"id": collection_id})
        session.commit()
        
        word = "Shiny ✨" if on else "Normal"
        click.echo(click.style(f"✓ Pokemon #{collection_id} is now {word}!", fg="cyan" if on else "white"))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))
        click.echo("Hint: Did you run 'python main.py db migrate' yet?")
    finally:
        session.close()


@trainer.command(name="level-up")
@click.argument("collection_id", type=int)
@click.option("--by", default=1, help="Number of levels to increase")
def level_up(collection_id: int, by: int):
    """Increase a Pokemon's level."""
    session = get_session()
    record = session.query(Collection).filter(Collection.id == collection_id).first()
    
    if not record:
        click.echo(click.style("✗ Collection record not found!", fg="red"))
        session.close()
        return

    new_level = record.level + by
    queries.update_collection_level(session, collection_id, new_level)
    
    click.echo(click.style(f"✓ {record.nickname or record.pokemon.name} leveled up to {new_level}!", fg="green"))
    session.close()


@trainer.command(name="release")
@click.argument("collection_id", type=int)
def release(collection_id: int):
    """Release a Pokemon from a trainer's collection."""
    session = get_session()
    record = session.query(Collection).filter(Collection.id == collection_id).first()
    
    if not record:
        click.echo(click.style("✗ Collection record not found!", fg="red"))
        session.close()
        return

    name = record.nickname or record.pokemon.name
    if click.confirm(f"Are you sure you want to release {name}?"):
        queries.delete_collection_record(session, collection_id)
        click.echo(click.style(f"✓ {name} was released into the wild.", fg="green"))
    
    session.close()


@cli.group()
def lab():
    """Advanced Lab tools for manual SQL and schema exploration."""
    pass


@lab.command(name="query")
@click.argument("sql_string")
def manual_query(sql_string: str):
    """Execute a raw SQL query and see the results (STRICTLY FOR LEARNING)."""
    from sqlalchemy import text
    session = get_session()
    
    try:
        result = session.execute(text(sql_string))
        
        # If it's a SELECT (has rows)
        if result.returns_rows:
            rows = result.fetchall()
            if not rows:
                click.echo("Query returned 0 rows.")
            else:
                # Print column headers
                click.echo(f"\n{click.style(' | '.join(result.keys()), bold=True, fg='cyan')}")
                click.echo("-" * 40)
                for row in rows:
                    click.echo(" | ".join(str(val) for val in row))
                click.echo(f"\nTotal: {len(rows)} results.\n")
        else:
            # For UPDATE/DELETE/INSERT
            session.commit()
            click.echo(click.style(f"✓ Command executed successfully. Rows affected: {result.rowcount}", fg="green"))
            
    except Exception as e:
        click.echo(click.style(f"✗ SQL Error: {str(e)}", fg="red"))
    finally:
        session.close()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    cli()
