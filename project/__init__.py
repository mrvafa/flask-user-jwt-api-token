import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig',
)
app.config.from_object('config.DevelopmentConfig')
CORS(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from project.User.api.urls import auth_blueprint

app.register_blueprint(auth_blueprint)
