# Pokedex Database Lab 🎮

Welcome to your first mission as a Database Researcher! This project is a hands-on lab designed to teach you the fundamentals of **Relational Databases** using the world of Pokemon.

You will learn how to:
1.  **Explore** data through a web interface.
2.  **Manipulate** data using a Command Line Interface (CLI).
3.  **Inspect** raw tables using professional tools like pgAdmin.
4.  **Query** the database directly using SQL (Structured Query Language).

---

## 🚀 Quick Start

### 1. Launch the Lab
Everything is pre-configured with **Docker**. Just run:

```bash
docker compose up -d
```

This starts four services:
-   **Database (Postgres)**: Where the data actually lives.
-   **Pokedex GUI (Flask)**: A web interface to view the data (`http://localhost:5000`).
-   **pgAdmin**: A professional database management tool (`http://localhost:8080`).
-   **Pokedex CLI**: A tool to interact with the database via commands.

### 2. Initialize and Seed
Before you can see any Pokemon, you need to set up the "schema" (the tables) and add some initial data.

```bash
# Enter the app container
docker exec -it pokedex_app bash

# Inside the container, run these commands:
python main.py db init
python main.py db seed
```

---

## 🗺️ Your Learning Path

### Mission 0: The Pokedex UI
Open your browser to [http://localhost:5000](http://localhost:5000).
-   Explore the Pokedex.
-   Check out the "Trainers" list.
-   View Ash Ketchum's profile to see his current team.

**Think about:** How is the data organized? How does the website know that Ash has a Pikachu?

### Mission 1: Command Line Mastery
Now, let's add some data ourselves. Stay inside the `docker exec` session:

```bash
# See all Pokemon
python main.py pokemon list

# Add your favorite Pokemon
python main.py pokemon add

# Register yourself as a trainer
python main.py trainer add

# Catch a Pokemon for your team!
python main.py catch <your_trainer_id> <pokemon_id> --nickname "Sparky"
```

Refresh the web UI to see your changes reflected immediately!

### Mission 2: Under the Hood (pgAdmin)
Professional developers use tools like **pgAdmin** to look at the "raw" tables.
1.  Go to [http://localhost:8080](http://localhost:8080).
2.  **Login**: `admin@pgadmin.org` / `admin`.
3.  **Connect to Server**:
    -   Right-click "Servers" > Register > Server.
    -   **Name**: Pokedex.
    -   **Connection tab**:
        -   **Host**: `db`
        -   **Maintenance DB**: `pokedex`
        -   **Username**: `postgres`
        -   **Password**: `postgres`
4.  **Explore**: Navigate to `Databases` > `pokedex` > `Schemas` > `public` > `Tables`.

---

## 🧪 Test-Driven Development (TDD)

Database integrity is crucial. We use **tests** to make sure our code doesn't accidentally break the rules of our database.

To run the tests:
```bash
docker compose run --rm test
```

### 🛠️ Your Assignment: Fix the Bug!
We have a bug in our system: **Pokemon can be created with negative Attack points!** This shouldn't be allowed in a fair tournament.

1.  Open `tests/test_pokedex.py`.
2.  Find the test case that is currently failing.
3.  Modify `src/models.py` or the CLI logic to ensure Attack values are always positive.

<details>
<summary><b>💡 Check your answer (Spoiler Alert!)</b></summary>

One of the most robust ways to fix this is by adding a **Check Constraint** to your database model in `src/models.py`. 

You can import `CheckConstraint` from SQLAlchemy and add it to your `Pokemon` class:

```python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint

class Pokemon(Base):
    __tablename__ = "pokemon"
    # ... other columns ...
    attack = Column(Integer, default=50)
    
    __table_args__ = (
        CheckConstraint('attack >= 0', name='check_attack_positive'),
    )
```

After making this change, you'll need to recreate the database (`db init`) for the constraint to take effect!
</details>

---

## 🏗️ Architecture

-   **Backend**: Python 3.13 + SQLAlchemy (ORM)
-   **Database**: PostgreSQL 15
-   **Web UI**: Flask + Bootstrap
-   **Infrastructure**: Docker & Docker Compose

## 📜 License
MIT
