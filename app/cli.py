import click
from rich.console import Console
from rich.table import Table

from app.models import auth as model
from app.storage.db import db


@click.group()
def show():
    """cli commands"""


@show.command('roles')
@click.option('--limit', type=click.IntRange(1, 50, clamp=True), default=20)
def list_roles(limit: int):
    """list roles"""
    table = Table(title='Roles')
    table.add_column('Name')
    table.add_column('Description')
    table.add_column('Updated')

    q = db.select(model.Role.name, model.Role.description,
                  model.Role.update_datetime).limit(limit)
    for row in db.session.execute(q):
        table.add_row(row[0], row[1], str(row[2]))

    console = Console()
    console.print(table)
