# Pokedex Database Lab (Postgres Example) 🎮

A teaching tool designed to demonstrate relational database concepts through a Pokemon-themed application. This repository provides a complete environment including a PostgreSQL database, a Flask web interface, a CLI management tool, and pgAdmin for direct database inspection.

> [!IMPORTANT]
> **Students & Learners:** For the guided lab instructions and missions, please see [**LESSON.md**](./LESSON.md).

---

## 🛠️ Project Overview

This lab demonstrates how different application layers interact with a relational database:
- **ORM (SQLAlchemy)**: How Python objects map to database tables.
- **Web UI (Flask)**: How data is queried and rendered in a browser.
- **CLI (Click)**: How to manage and manipulate data via the terminal.
- **Raw SQL (pgAdmin)**: How to inspect and query data directly.

---

## 🏗️ Technical Architecture

- **Database**: [PostgreSQL 15](https://www.postgresql.org/)
- **Backend**: Python 3.13 with [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Web Interface**: [Flask](https://flask.palletsprojects.com/) + [Bootstrap 5](https://getbootstrap.com/)
- **CLI Framework**: [Click](https://click.palletsprojects.com/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- **Testing**: [Pytest](https://docs.pytest.org/)

---

## 🚀 Getting Started

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine installed.
- [Git](https://git-scm.com/) installed.

### 2. Setup
Clone the repository and launch the environment:

```bash
git clone https://github.com/RiceC-at-MasonHS/postgres_example_db.git
cd postgres-example-db
docker compose up -d
```

This starts the following services:
- **Pokedex GUI**: [http://localhost:5000](http://localhost:5000)
- **pgAdmin**: [http://localhost:8080](http://localhost:8080) (User: `admin@pgadmin.org` / Pass: `admin`)
- **Database (Postgres)**: Internal port `5432`

### 3. Initialize the Database
Set up the schema and seed initial data:

```bash
docker exec -it pokedex_app python main.py db init
docker exec -it pokedex_app python main.py db seed
```

---

## 🧪 Development & Testing

To run the automated test suite:
```bash
docker compose run --rm test
```

For more details on specific missions and the TDD assignment, refer to the [**LESSON.md**](./LESSON.md) file.

---

## 📜 License
MIT
