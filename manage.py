from application import db
import click
from flask import Flask

app = Flask(__name__)

@app.cli.command("init-db")
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo("Initialized the database.")

@app.cli.command("drop-db")
def drop_db_command():
    """Drop all tables in the database."""
    db.drop_all()
    click.echo("Dropped the database.")
