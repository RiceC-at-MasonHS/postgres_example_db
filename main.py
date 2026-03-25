#!/usr/bin/env python3
"""
Entry point for the Postgres Teaching CLI application.
Run: python -m src.cli <command> <args>
Or: python main.py <command> <args>
"""

from src.cli import cli

if __name__ == "__main__":
    cli()
