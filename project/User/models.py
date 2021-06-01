import binascii
import os
from datetime import datetime, timedelta

import jwt
from werkzeug.routing import ValidationError

from project import db, bcrypt, app
from project.Validators import username_validation, password_validation, email_validation


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.now()
        self.token = binascii.hexlify(os.urandom(20)).decode()

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=10),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def create(**kwargs):
        User.check_validation(**kwargs)
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def check_validation(**kwargs):
        errors = []
        if 'password' not in kwargs:
            errors.append('Password is required!')
        elif not password_validation(kwargs['password']):
            errors.append('Minimum eight characters, at least one letter, one number and one special character!')
        if 'email' not in kwargs:
            errors.append('Email is required!')
        elif not email_validation(kwargs['email']):
            errors.append('Email address is not valid!')
        if 'username' not in kwargs:
            errors.append('Username is required!')
        elif not username_validation(kwargs['username']):
            errors.append('Invalid username (username length should be between 4, 30, not . _ at first and combination '
                          'of characters)')
        if errors:
            raise ValidationError(errors)
