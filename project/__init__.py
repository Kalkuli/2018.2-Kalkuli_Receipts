import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Instantiate the app
app = Flask(__name__)


# Set Configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


# Instanciate Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from project.api.views import receipts_blueprint
app.register_blueprint(receipts_blueprint)
