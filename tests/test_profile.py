import unittest
from app import create_app, db
from app.models import User, PromptEntry

class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # Set up a test user
        self.user = User(username='test_director', email='director@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

        # Set up prompt for user
        self.prompt = PromptEntry(
            title='Test Director Prompt',
            original_prompt='cinematic portrait of test director',
            user_id=self.user.id
        )
        db.session.add(self.prompt)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_profile_page_success(self):
        response = self.client.get('/profile/test_director')
        self.assertEqual(response.status_code, 200)
        # Check that the username is displayed on the page
        self.assertIn('test_director', response.data.decode('utf-8'))
        # Check that the user's prompt title is displayed
        self.assertIn('Test Director Prompt', response.data.decode('utf-8'))

    def test_profile_page_not_found(self):
        response = self.client.get('/profile/non_existent_user')
        self.assertEqual(response.status_code, 404)
        # Check that our custom 404 page is rendered
        self.assertIn('Aradığınız sahne mevcut değil', response.data.decode('utf-8'))
