from flask_testing import TestCase
from werkzeug.routing import ValidationError

from project import app, db
from project.User.models import User


class TestUser(TestCase):
    def test_ok_create_user(self):
        user = User.create(username='user1', password='2AsSWPdJdzVh99Me', email='user1@domain.com')
        self.assertEqual(User.query.filter_by(username='user1').first(), user)

    def test_wrong_create_user_no_password(self):
        with self.assertRaises(ValidationError):
            User.create(username='user2', email='user2@domain.com')

    def test_wrong_create_user_no_email(self):
        with self.assertRaises(ValidationError):
            User.create(username='user3', password='ee8Ft6F9T2qFCTGG')

    def test_wrong_create_user_no_username(self):
        with self.assertRaises(ValidationError):
            User.create(email='user4@domain.com', password='8bjykFxxzYracyqa')

    def test_wrong_create_user_wrong_email(self):
        with self.assertRaises(ValidationError):
            User.create(username='user5', email='user5@domain', password='a7w85wfaYhuRGDVs')

    def test_wrong_create_user_wrong_username(self):
        with self.assertRaises(ValidationError):
            User.create(username='6', email='user6@domain', password='92VQjLrvCXfrHLnN')

    def test_wrong_create_user_wrong_password(self):
        with self.assertRaises(ValidationError):
            User.create(username='user7', email='user7@domain', password='11111111111')

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
