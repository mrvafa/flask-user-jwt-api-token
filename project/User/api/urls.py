from flask import Blueprint

from project.User.api.views import RegisterAPI, LoginAPI, UserProfileAPI
auth_blueprint = Blueprint('user', __name__)

registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
profile_view = UserProfileAPI.as_view('profile_api')

auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST'],
)

auth_blueprint.add_url_rule(
    '/profile/<user_id>',
    view_func=profile_view,
    methods=['GET'],
)

auth_blueprint.add_url_rule(
    '/profile',
    view_func=profile_view,
    methods=['PUT'],
)
