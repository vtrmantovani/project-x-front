from pxf import db
from pxf.models.user import User
from tests.base import BaseTestCase


class TestModelWebsite(BaseTestCase):

    def test_create_website(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        user.enabled = True
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)

    def test_validate_email(self):
        with self.assertRaisesRegexp(ValueError, "Email is invalid"):
            User(email="vtrmantovani", password="123456")

        with self.assertRaisesRegexp(ValueError, "Email is required"):
            User(email="", password="123456")

        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertEqual(user.email, "vtrmantovani@gmail.com")

    def test_validate_password(self):

        with self.assertRaisesRegexp(ValueError, "Password is required"):
            user = User(email="vtrmantovani@gmail.com", password="")

        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertIsNotNone(user.password)
