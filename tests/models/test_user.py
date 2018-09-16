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
            User(email="vtrmantovani@gmail.com", password="")

        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertIsNotNone(user.password)

    def test_check_password(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertTrue(user.check_password("123456"))

    def test_check_password_false_case(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertFalse(user.check_password("xpto"))

    def test_is_authenticated(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertFalse(user.is_authenticated())

    def test_is_active(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        with self.assertRaises(AttributeError):
            self.assertFalse(user.is_active())

    def test_is_anonymous(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertTrue(user.is_anonymous())

    def test_get_id(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        self.assertEquals(user.get_id(), None)

    def test_reload(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        user.enabled = True
        db.session.add(user)
        db.session.commit()
        user.reload()

    def test_load_user(self):
        user = User(email="vtrmantovani@gmail.com", password="123456")
        user.load_user(1)
