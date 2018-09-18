from flask.cli import FlaskGroup
from project import app, db
from project.api.models import Receipt, Product

cli = FlaskGroup(app)


# Create command
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()