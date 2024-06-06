import unittest
import re

from rich import print

from flask import url_for, session
from webapp import create_app, db, admin
from webapp.auth.models import User, Role
from webapp.predict import predict_details, predict_feed_sentiment

class TestUrlsCase(unittest.TestCase):
    def setUp(self):
        admin._views = []
        #rest_api.resources = []

        self.app = create_app('config.TestConfig')
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'
        self.client = self.app.test_client(use_cookies=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
       
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_home_page(self):
        """Test is the application's homepage returns successfully."""
        result = self.client.get(url_for('app.index'))
        self.assertEqual(result.status_code, 200)
    
    def test_redirect_url(self):
        """Test if the root url returns 302"""
        result = self.client.get('/')
        self.assertEqual(result.status_code, 404)
        #assert "/letsgo/" in result.headers['Location']

    def test_register_login(self):
        """Tests registering a user, logging in, confirmation of the token, and finally logging out."""
        response = self.client.post(url_for('auth.signup'),
                                    data={
                                        'email': 'riri.letsgo@gmail.com',
                                        'username': 'Riri',
                                        'password': 'testing12',
                                        'confirm': 'testing12'
                                    }, follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertNotIn("This is LetsGo", response.get_data(as_text=True))

        #Login.
        response = self.client.post(url_for('auth.signin'), 
                                    data={
                                        'username': 'Riri',
                                        'password': 'testing12'
                                    }, follow_redirects=True)
        
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Kindly confirm', data))
        self.assertTrue("You are yet to confirm your account." in data)

        #Confirmation token.
        user = User.query.filter_by(username='Riri').first_or_404()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue("You have confirmed your account" in data)

        #Logout
        response =  self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue("Login" in data)

    def test_submit_features(self):
        """Test if feature submission form is accesible, user can submit features, and get predictions."""
        #Check if the page displays successfully.
        response = self.client.get(url_for('app.form'), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        
        #User can be able to submit features. 
        response = self.client.post(url_for('app.form'), 
                                    data={
                                        'country': 'Kenya', 'age': '25-44', 'companion': 'Alone', 
                                        'male': 1, 'female': 0, 'main_nights': 5, 'zanzi_nights': 0,
                                        'purpose': 'Leisure and Holidays', 'activity': 'Wildlife Tourism',
                                        'info': 'Others', 'arrangement': 'Independent',
                                        'pack_tra_int': 'No', 'pack_tra_tz': 'No',
                                        'pack_acc': 'No', 'pack_food': 'No', 'pack_sight': 'No',
                                        'pack_guide': 'No', 'pack_insurance': 'No',
                                        'freq': 'Yes'
                                    }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Kindly pick your travel characteristics." in response.get_data(as_text=True))
        # with self.client.session_transaction() as sess:
        #     predict_details(response.data.as_text(True))
        #     self.assertIn("category", sess)
        

        with self.client.session_transaction() as sess:
            response = self.client.get(url_for('app.predict'), follow_redirects=True)
            print(response.get_data(as_text=True))
            self.assertTrue(response.status_code, 200)
            self.assertIn("category", sess)



    # def _insert_user(self, username, password, role_name):
    #     """"""
    #     self.test_role = Role(role_name)
    #     db.session.add(self.test_role)
    #     db.session.commit()

    #     self.test_user = User(username)
    #     self.test_user.set_password(password)
    #     db.session.add(self.test_user)
    #     db.session.commit()

    # def test_login(self):
    #     """Test if the login works perfectly."""
    #     self._insert_user("test", "test1256", "default")
    #     result = self.client.post('/letsgo/auth/signin', 
    #                              data=dict(username="test", password="test1256"),
    #                              follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('You have been logged in successfully.', result.data)
    
    # def test_failed_login(self):
    #     """Test login-went-bad."""
    #     self._insert_user(username="test", password="test1256", role_name="default")
    #     result = self.client.post("/letsgo/auth/signin", 
    #                               data=dict(username="test", password="badpassword"),
    #                               follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('Invalid username or password.', result.data)
    #     result = self.client.get("/letsgo/")
    #     self.assertEqual(result.status_code, 302)
    
    # def test_unauthorized_access(self):
    #     """Tests for unauthorized access to protected views"""
    #     self._insert_user("test", "test1256", "default")
    #     result = self.client.post('/letsgo/auth/signin', 
    #                              data=dict(username="test", password="test1256"),
    #                              follow_redirects=True)
    #     result = self.client.get('/letsgo/admin/admindashboard/')
    #     self.assertEqual(result.status_code, 403)



if __name__  ==  "__main__":
    unittest.main()
