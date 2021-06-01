import json
import time

from flask import url_for
from flask_testing import TestCase
from project import app, db
from project.User.models import User


class TestUserRegisterAPI(TestCase):
    def test_ok_create_user(self):
        data = json.dumps({'username': 'user1', 'password': 'YVmx99BUMeEt8Q45', 'email': 'user1@domain.com'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(201, respond.status_code)

    def test_wrong_create_user_no_password(self):
        data = json.dumps({'username': 'user2', 'email': 'user2@domain.com'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_empty_password(self):
        data = json.dumps({'username': 'user3', 'password': '', 'email': 'user3@domain.com'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_easy_password(self):
        data = json.dumps({'username': 'user4', 'password': '1111111111', 'email': 'user4@domain.com'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_no_username(self):
        data = json.dumps({'email': 'user5@domain.com', 'password': 'v5Xj9FEveYeUtkcT'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_empty_username(self):
        data = json.dumps({'password': '3WLqY5ZEH2pU3WVJ', 'username': '', 'email': 'user6@domain.com'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_incorrect_username(self):
        data = json.dumps({'username': '7', 'password': 'G2KzJduYQQYWsxfk', 'email': 'user7@domain.com'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_no_email(self):
        data = json.dumps({'username': 'user8', 'password': '32EfkNTXksPZBV2a'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_empty_email(self):
        data = json.dumps({'password': '3WLqY5ZEH2pU3WVJ', 'email': '', 'username': 'user9'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_incorrect_email(self):
        data = json.dumps({'email': '1', 'password': 'G2KzJduYQQYWsxfk', 'username': 'user10'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_exists_username(self):
        User.create(username='test_user', password='hutqnYcDTJ9yqANc', email='test_user@domain.com')
        data = json.dumps({'email': 'user11@domain.com', 'password': 'nY9Zyh3tkPL6kN3b', 'username': 'test_user'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def test_wrong_create_user_exists_email(self):
        User.create(username='test_user', password='hutqnYcDTJ9yqANc', email='test_user@domain.com')
        data = json.dumps({'email': 'test_user@domain.com', 'password': 'QR2T4eZAevL9ucvr', 'username': 'user12'})
        respond = self.client.post(url_for('user.register_api'), data=data, content_type='application/json')
        self.assertEqual(400, respond.status_code)

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestUserLoginAPI(TestCase):
    def test_ok_user_login_check_respond(self):
        respond = self.client.post(url_for('user.login_api'), data=self.user_1_data, content_type='application/json')
        self.assertEqual(200, respond.status_code)

    def test_ok_user_login_check_username(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({'username': 'user1', 'password': 'mCWwfhBnt2G4WDtQ'})
                                   )
        self.assertEqual(200, respond.status_code)

    def test_ok_user_login_check_email(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({'email': 'user1@domain.com', 'password': 'mCWwfhBnt2G4WDtQ'})
                                   )
        self.assertEqual(200, respond.status_code)

    def test_ok_user_login_check_token(self):
        respond = self.client.post(url_for('user.login_api'), data=self.user_1_data, content_type='application/json')
        self.assertTrue(respond.json['token'] is not None)

    def test_wrong_user_login_true_email_wrong_username(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({
                                       'username': 'wrong_user_name',
                                       'email': 'user1@domain.com',
                                       'password': 'mCWwfhBnt2G4WDtQ'})
                                   )
        self.assertEqual(400, respond.status_code)

    def test_wrong_user_login_true_username_wrong_login(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({
                                       'username': 'user1',
                                       'email': 'wrong_email@domain.com',
                                       'password': 'mCWwfhBnt2G4WDtQ'})
                                   )
        self.assertEqual(400, respond.status_code)

    def test_ok_user_login_check_token_different_after_login_again(self):
        old_respond = self.client.post(url_for('user.login_api'), data=self.user_1_data,
                                       content_type='application/json')
        time.sleep(1)
        new_respond = self.client.post(url_for('user.login_api'), data=self.user_1_data,
                                       content_type='application/json')
        self.assertNotEqual(old_respond.json['token'], new_respond.json['token'])

    def test_wrong_login_wrong_password(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({'username': 'user1', 'password': 'wrong_password'}))
        self.assertEqual(400, respond.status_code)

    def test_wrong_login_wrong_username(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({'username': 'wrong_username', 'password': 'mCWwfhBnt2G4WDtQ'}))
        self.assertEqual(400, respond.status_code)

    def test_wrong_login_wrong_username_password(self):
        respond = self.client.post(url_for('user.login_api'), content_type='application/json',
                                   data=json.dumps({'username': 'wrong_username', 'password': 'wrong_password'}))
        self.assertEqual(400, respond.status_code)

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        self.user_1_data = json.dumps(
            {'username': 'user1', 'password': 'mCWwfhBnt2G4WDtQ', 'email': 'user1@domain.com'}
        )
        self.user_1 = User.create(username='user1', password='mCWwfhBnt2G4WDtQ', email='user1@domain.com')

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestGetUserProfile(TestCase):
    def test_get_ok_profile(self):
        respond = self.client.get(url_for('user.profile_api', user_id=1), )
        self.assertEqual(200, respond.status_code)

    def test_get_ok_profile_check_data(self):
        respond = self.client.get(url_for('user.profile_api', user_id=2), )
        username = User.query.filter_by(id=2).first().username
        email = User.query.filter_by(id=2).first().email
        user_id = User.query.filter_by(id=2).first().id
        print(respond.json)
        self.assertEqual(username, respond.json['username'])
        self.assertEqual(email, respond.json['email'])
        self.assertEqual(user_id, respond.json['user_id'])

    def test_get_ok_profile_not_contain_password(self):
        respond = self.client.get(url_for('user.profile_api', user_id=1), )
        self.assertFalse('username' not in respond.json)

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        self.user_1 = User.create(username='user1', password='qqhpqq9Ev7CUgGQP', email='user1@domain.com')
        self.user_2 = User.create(username='user2', password='eQk9qFZC3yWLdy9Q', email='user2@domain.com')
        self.user_3 = User.create(username='user3', password='YM9qEcH93XwvpzET', email='user3@domain.com')

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestEditUserProfile(TestCase):
    def test_get_ok_profile(self):
        token = self.client.post(
            url_for('user.login_api'), content_type='application/json',
            data=json.dumps(
                {'password': 'qqhpqq9Ev7CUgGQP', 'email': 'user1@domain.com'}
            )).json['token']
        respond = self.client.put(url_for('user.profile_api'), headers={
            'Authorization': f'Token {token}',
        }, )
        self.assertEqual(202, respond.status_code)

    def test_get_ok_profile_change_username(self):
        token = self.client.post(
            url_for('user.login_api'), content_type='application/json',
            data=json.dumps(
                {'password': 'qqhpqq9Ev7CUgGQP', 'email': 'user1@domain.com'}
            )).json['token']

        respond = self.client.put(
            url_for('user.profile_api'),
            content_type='application/json',
            data=json.dumps({'username': 'user11'}),
            headers={
                'Authorization': f'Token {token}',
            },
        )

        self.assertEqual(202, respond.status_code)
        self.assertIsNone(User.query.filter_by(username='user1').first())
        self.assertIsNotNone(User.query.filter_by(username='user11').first())

    def test_get_ok_profile_change_email(self):
        token = self.client.post(
            url_for('user.login_api'), content_type='application/json',
            data=json.dumps(
                {'password': 'qqhpqq9Ev7CUgGQP', 'email': 'user1@domain.com'}
            )).json['token']

        respond = self.client.put(
            url_for('user.profile_api'),
            content_type='application/json',
            data=json.dumps({'email': 'user11@domain.com'}),
            headers={
                'Authorization': f'Token {token}',
            },
        )

        self.assertEqual(202, respond.status_code)
        self.assertIsNone(User.query.filter_by(email='user1@domain.com').first())
        self.assertIsNotNone(User.query.filter_by(email='user11@domain.com').first())

    def test_get_ok_profile_change_email_username(self):
        token = self.client.post(
            url_for('user.login_api'), content_type='application/json',
            data=json.dumps(
                {'password': 'qqhpqq9Ev7CUgGQP', 'email': 'user1@domain.com'}
            )).json['token']

        respond = self.client.put(
            url_for('user.profile_api'),
            content_type='application/json',
            data=json.dumps({'email': 'user11@domain.com', 'username': 'user11'}),
            headers={
                'Authorization': f'Token {token}',
            },
        )

        self.assertEqual(202, respond.status_code)
        self.assertIsNone(User.query.filter_by(email='user1@domain.com').first())
        self.assertIsNotNone(User.query.filter_by(email='user11@domain.com', username='user11').first())

    def test_get_wrong_profile_change_email_taken(self):
        token = self.client.post(
            url_for('user.login_api'), content_type='application/json',
            data=json.dumps(
                {'password': 'qqhpqq9Ev7CUgGQP', 'email': 'user1@domain.com'}
            )).json['token']

        respond = self.client.put(
            url_for('user.profile_api'),
            content_type='application/json',
            data=json.dumps({'email': 'user2@domain.com'}),
            headers={
                'Authorization': f'Token {token}',
            },
        )

        self.assertEqual(400, respond.status_code)

    def test_get_wrong_profile_change_username_taken(self):
        token = self.client.post(
            url_for('user.login_api'), content_type='application/json',
            data=json.dumps(
                {'password': 'qqhpqq9Ev7CUgGQP', 'email': 'user1@domain.com'}
            )).json['token']

        respond = self.client.put(
            url_for('user.profile_api'),
            content_type='application/json',
            data=json.dumps({'username': 'user2'}),
            headers={
                'Authorization': f'Token {token}',
            },
        )

        self.assertEqual(400, respond.status_code)

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        self.user_1 = User.create(username='user1', password='qqhpqq9Ev7CUgGQP', email='user1@domain.com')
        self.user_2 = User.create(username='user2', password='eQk9qFZC3yWLdy9Q', email='user2@domain.com')
        self.user_3 = User.create(username='user3', password='YM9qEcH93XwvpzET', email='user3@domain.com')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
