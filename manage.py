from flask.cli import FlaskGroup
from project import app, db
from project.api.models import Receipt, Product
import unittest

cli = FlaskGroup(app)


# Create command
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# Registers comand to run tests
@cli.command()
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()