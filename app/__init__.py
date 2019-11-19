import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l


flask_app = Flask(__name__)
flask_app.config.from_object(Configuration)
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)
login = LoginManager(flask_app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
bootstrap = Bootstrap(flask_app)
moment = Moment(flask_app)
babel = Babel(flask_app)

from app import routes, models, errors

if not flask_app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    flask_app.logger.addHandler(file_handler)

    flask_app.logger.setLevel(logging.INFO)
    flask_app.logger.info('Microblog Startup...')


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(flask_app.config['LANGUAGES'])
