import unittest
from webapp import create_app, db, admin
from webapp.auth.models import User, Role

class TestUrlsCase(unittest.TestCase):
    def setUp(self):
        admin._views = []
        #rest_api.resources = []

        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.app = db
        db.create_all()

    def tearDown(self):
        db.session.remove()
    def test_home_page(self):
        """Test is the application's homepage returns successfully."""
        result = self.client.get('/letsgo/')
        self.assertEqual(result.status_code, 200)
    
    def test_redirect_url(self):
        """Test if the root url returns 302"""
        result = self.client.get('/')
        self.assertEqual(result.status_code, 404)
        #assert "/letsgo/" in result.headers['Location']

    def _insert_user(self, username, password, role_name):
        """"""
        test_role = Role(role_name)
        db.session.add(test_role)
        db.session.commit()

        test_user = User(username)
        test_user.set_password(password)
        db.session.add(test_user)
        db.session.commit()

    def test_login(self):
        """Test if the login works perfectly."""
        result = self.client.post('/letsgo/auth/signin', 
                                 data=dict(username="test", password="test"),
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('You have been logged in successfully.', result.data)
    
    def test_failed_login(self):
        """Test login-went-bad."""
        result = self.client.post("/letsgo/auth/signin", 
                                  data=dict(username="test", password="badpassword"),
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Invalid username or password.', result.data)
        result = self.client.get("/letsgo/")
        self.assertEqual(result.status_code, 302)
        



if __name__  ==  "__main__":
    unittest.main()
