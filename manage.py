import coverage

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()

from flask.cli import FlaskGroup
from project import app, db
import unittest
from populate import seedReceipts, seedTags

cli = FlaskGroup(app)


# Create command
@cli.command()
def recreatedb():
    db.drop_all()
    db.create_all()
    db.session.commit()

# Populate Functions
@cli.command()
def seed():
    seedTags(db)
    seedReceipts(db)


# Registers comand to run tests
@cli.command()
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.xml_report()
        return 0
    return 1


if __name__ == '__main__':
    cli()
