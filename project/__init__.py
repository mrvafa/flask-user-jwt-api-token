import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite3'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
from project.User.api.urls import auth_blueprint
app.register_blueprint(auth_blueprint)
