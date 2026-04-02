# Pokedex Database Lab (Postgres Example) 🎮

A teaching tool designed to demonstrate relational database concepts through a Pokemon-themed application. This repository provides a complete environment including a PostgreSQL database, a Flask web interface, a CLI management tool, and pgAdmin for direct database inspection.

> [!IMPORTANT]
> **Students & Learners:** For the guided lab instructions and missions, please see [**LESSON.md**](./LESSON.md).
> 
> ------------------------ Then proceed onto [**LESSON_ADVANCED.md**](./LESSON_ADVANCED.md) if directed to do so.

![PostgreSQL Elephant Logo](https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg)

### The Gold-Standard Database: PostgreSQL

PostgreSQL (often simply called **Postgres**) is widely considered the "gold-standard" for relational databases. But what makes it so special?

-   **Reliability and Data Integrity**: Postgres is built with a "data-first" philosophy, ensuring that your information remains consistent even in the event of a system crash.
-   **Extensibility**: It's incredibly flexible, allowing users to define their own data types, index types, and even write code in different languages that runs directly inside the database.
-   **Open Source Community**: With over 35 years of active development, Postgres has one of the most mature and supportive open-source communities in the world.
-   **Advanced Features**: It supports complex queries, JSON data handling, and sophisticated concurrency control that many other databases are still catching up to.

### 🐳 Docker: Your Personal Lab Sandbox

This entire project is built using **Docker containers**. Think of Docker as a way to package up an entire computer system (including the database, the web server, and all the tools) into a small, portable "container."

-   **Consistency**: Whether you're on Windows, macOS, or Linux, the project will run exactly the same way.
-   **Safety**: Everything stays inside the container, so you don't have to worry about accidentally "breaking" your own computer's settings or installing complex software locally.
-   **The "Sandbox" Effect**: Docker provides a perfect sandbox for beginners. You can experiment, delete things, and start over in seconds, making it a low-risk environment for learning how databases work in the real world. 


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

These instructions are repeating the start of the [**LESSON.md**](./LESSON.md), in case you can't wait to get started. 

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine installed.
- [Git](https://git-scm.com/) installed.

### 2. Setup
Clone the repository and launch the environment:

```bash
git clone https://github.com/RiceC-at-MasonHS/postgres_example_db.git
cd postgres_example_db
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

GPL-3.0 License
