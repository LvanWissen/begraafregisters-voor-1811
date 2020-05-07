import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

# from app import models, views, routes

__version__ = "0.1"


class Config(object):

    # General config
    SECRET_KEY = "4666a91e32434fd795c81dac7e8e3a8f"

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ.get('APP_USER', 'postgres')}:{os.environ.get('APP_PASSWORD', 'example')}@{os.environ.get('APP_DBSERVER', 'localhost')}:{os.environ.get('APP_DBPORT', '8123')}/{os.environ.get('APP_DB', 'begraafregisters')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Flask-Admin config
    FLASK_ADMIN_SWATCH = 'flatly'

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Begraafregisters', template_mode='bootstrap3')
import begraafregisters.views

__exports__ = [app, db, admin]
