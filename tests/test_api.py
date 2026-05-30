import unittest
import json
from app import create_app, db
from app.models import User, PromptEntry, Tag

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        self.user = User(username='api_user', email='api@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

        # Create some test prompts with tags
        self.tag = Tag(name='cyberpunk')
        db.session.add(self.tag)
        db.session.commit()

        for i in range(12):
            p = PromptEntry(
                title=f'Prompt Title {i}',
                original_prompt=f'original prompt content {i}',
                user_id=self.user.id
            )
            p.tags.append(self.tag)
            db.session.add(p)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_prompts_endpoint(self):
        response = self.client.get('/api/v1/prompts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        
        # We queried the latest 10, so it should return exactly 10 prompts
        self.assertEqual(len(data), 10)
        
        # Verify the structure of the first prompt
        first_prompt = data[0]
        self.assertIn('id', first_prompt)
        self.assertIn('title', first_prompt)
        self.assertIn('original_prompt', first_prompt)
        self.assertIn('author', first_prompt)
        self.assertIn('tags', first_prompt)
        
        self.assertEqual(first_prompt['author'], 'api_user')
        self.assertIn('cyberpunk', first_prompt['tags'])
