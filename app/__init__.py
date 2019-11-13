from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


flask_app = Flask(__name__)
flask_app.config.from_object(Configuration)
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

from app import routes, models
