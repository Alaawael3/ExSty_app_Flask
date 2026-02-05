import click
from flask.cli import with_appcontext
from Exsty_app import create_app, db

app = create_app()

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
    click.echo("Tables created successfully!")

app.cli.add_command(create_tables)

if __name__ == '__main__':
    app.run(debug=True)
