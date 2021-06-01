from flask import request, make_response, jsonify
from flask.views import MethodView
from werkzeug.routing import ValidationError

from project import db, bcrypt
from project.User.models import User


class RegisterAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username') if post_data and 'username' in post_data else None
        email = post_data.get('email') if post_data and 'email' in post_data else None
        password = post_data.get('password') if post_data and 'password' in post_data else None
        if not username or not email or not password:
            response_object = {
                'error': 'username, email and password is required',
            }
            return make_response(jsonify(response_object)), 400

        user_username = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if not user_username and not user_email:
            try:
                User.create(
                    username=username,
                    email=email,
                    password=password
                )
                response_object = {
                    'success': 'User has been created. now try to login.'
                }
                return make_response(jsonify(response_object)), 201
            except ValidationError as e:
                response_object = {
                    'error': f'{e}'
                }
                return make_response(jsonify(response_object)), 400

        else:
            response_object = {
                'error': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(response_object)), 400


class LoginAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username') if post_data and 'username' in post_data else None
        email = post_data.get('email') if post_data and 'email' in post_data else None
        password = post_data.get('password') if post_data and 'password' in post_data else None
        if not password or not (username or email):
            response_object = {
                'error': 'Password and email or username is required.',
            }
            return make_response(jsonify(response_object)), 400
        if username and not email:
            user = User.query.filter_by(
                username=username
            ).first()
            if user and bcrypt.check_password_hash(
                    user.password, password
            ):
                token = user.encode_auth_token()
                response_object = {
                    'token': token.decode()
                }
                return make_response(jsonify(response_object)), 200

        if email and not username:
            user = User.query.filter_by(
                email=email
            ).first()
            if user and bcrypt.check_password_hash(
                    user.password, password
            ):
                response_object = {
                    'token': user.encode_auth_token().decode(),
                }
                return make_response(jsonify(response_object)), 200

        if email and username:
            user = User.query.filter_by(username=username).first()
            if user and User.query.filter_by(email=email).first() == user:
                if user and bcrypt.check_password_hash(
                        user.password, password
                ):
                    token = user.encode_auth_token()
                    response_object = {
                        'token': token.decode()
                    }
                    return make_response(jsonify(response_object)), 200

        response_object = {
            'error': 'combination of User/Password is wrong'
        }
        return make_response(jsonify(response_object)), 400


class UserProfileAPI(MethodView):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            response_object = {
                'profile': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'registered_on': user.registered_on
                }
            }
            return make_response(jsonify(response_object)), 200
        return make_response(jsonify({"error": "page not found"})), 404

    def put(self):
        auth_header = request.headers.get('Authorization')
        auth_token = ''
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'error': 'Bearer token malformed.'
                }
                return make_response(jsonify(response_object)), 401

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                post_data = request.get_json()
                username = post_data.get('username') if post_data and 'username' in post_data else None
                email = post_data.get('email') if post_data and 'email' in post_data else None
                errors = []
                if email:
                    if User.query.filter_by(email=email).first() and user.email == email:
                        user.email = email
                    else:
                        errors.append('email has taken')
                if username:
                    if User.query.filter_by(username=username).first() and user.username == username:
                        user.username = username
                    else:
                        errors.append('username has taken')
                if errors:
                    return make_response(jsonify({"errors": errors})), 400
                else:
                    response_object = {
                        'profile': {
                            'user_id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'registered_on': user.registered_on
                        }
                    }
                    return make_response(jsonify(response_object)), 202
            response_object = {
                'error': resp
            }
            return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'error': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 401
