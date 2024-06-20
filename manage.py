from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def create_db():
    db.create_all()

@cli.command()
def drop_db():
    db.drop_all()

if __name__ == '__main__':
    cli()
