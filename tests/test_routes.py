import unittest
from sqlalchemy import select
from app import create_app, db
from app.models import User, PromptEntry, Tag, AIDiaryEntry


class RoutesTestCase(unittest.TestCase):
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

        # Set up a second test user (for permission tests)
        self.other_user = User(username='other_director', email='other@example.com')
        self.other_user.set_password('password123')
        db.session.add(self.other_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username='test_director', password='password123'):
        return self.client.post('/auth/login', data={
            'username_or_email': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def test_index_page(self):
        # Add some dummy prompts
        p1 = PromptEntry(title='Neon Cyberpunk', original_prompt='neon street portrait', user_id=self.user.id)
        p2 = PromptEntry(title='35mm Classic Film', original_prompt='classic noir street', user_id=self.other_user.id)
        db.session.add_all([p1, p2])
        db.session.commit()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Neon Cyberpunk', response.data)
        self.assertIn(b'35mm Classic Film', response.data)

    def test_index_pagination(self):
        import datetime
        # Add 12 dummy prompts with increasing created_at
        prompts = []
        base_time = datetime.datetime.utcnow()
        for i in range(12):
            p = PromptEntry(
                title=f'Prompt-{i:02d}',
                original_prompt=f'Original prompt content {i}',
                user_id=self.user.id,
                created_at=base_time + datetime.timedelta(seconds=i)
            )
            prompts.append(p)
        db.session.add_all(prompts)
        db.session.commit()

        # Page 1 should contain 10 items (from 2 to 11 due to descending order)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prompt-11', response.data)
        self.assertIn(b'Prompt-02', response.data)
        self.assertNotIn(b'Prompt-01', response.data)
        self.assertNotIn(b'Prompt-00', response.data)
        # Should have a next page link
        self.assertIn(b'page=2', response.data)
        self.assertIn(b'Sonraki', response.data)

        # Page 2 should contain the remaining 2 items (0 and 1)
        response = self.client.get('/?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prompt-01', response.data)
        self.assertIn(b'Prompt-00', response.data)
        self.assertNotIn(b'Prompt-11', response.data)
        # Should have a previous page link
        self.assertIn(b'page=1', response.data)
        self.assertIn(b'&laquo; \xc3\x96nceki', response.data)

    def test_index_search(self):
        p1 = PromptEntry(title='Neon Cyberpunk', original_prompt='neon street portrait', user_id=self.user.id)
        p2 = PromptEntry(title='35mm Classic Film', original_prompt='classic noir street', user_id=self.other_user.id)
        db.session.add_all([p1, p2])
        db.session.commit()

        response = self.client.get('/?q=cyberpunk')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Neon Cyberpunk', response.data)
        self.assertNotIn(b'35mm Classic Film', response.data)

    def test_index_tag_filter(self):
        p1 = PromptEntry(title='Neon Cyberpunk', original_prompt='neon street portrait', user_id=self.user.id)
        p2 = PromptEntry(title='35mm Classic Film', original_prompt='classic noir street', user_id=self.other_user.id)
        t = Tag(name='cyberpunk')
        db.session.add_all([p1, p2, t])
        db.session.commit()

        p1.tags.append(t)
        db.session.commit()

        response = self.client.get('/?tag=cyberpunk')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Neon Cyberpunk', response.data)
        self.assertNotIn(b'35mm Classic Film', response.data)

    def test_prompt_crud_anonymous(self):
        # Cannot add prompt
        response = self.client.get('/prompt/new')
        self.assertEqual(response.status_code, 302)  # Redirects to login

        # Can view details
        p = PromptEntry(title='Test Detail', original_prompt='some prompt text', user_id=self.user.id)
        db.session.add(p)
        db.session.commit()
        response = self.client.get(f'/prompt/{p.id}')
        self.assertEqual(response.status_code, 200)

        # Cannot edit
        response = self.client.get(f'/prompt/{p.id}/edit')
        self.assertEqual(response.status_code, 302)

        # Cannot delete
        response = self.client.post(f'/prompt/{p.id}/delete')
        self.assertEqual(response.status_code, 302)

    def test_prompt_creation(self):
        self.login()
        response = self.client.post('/prompt/new', data={
            'title': 'Golden Hour Portrait',
            'original_prompt': 'A scenic golden hour portrait, 85mm lens',
            'negative_prompt': 'blurry, dark',
            'tags': '85mm lens, golden hour, cinematic'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        p = PromptEntry.query.filter_by(title='Golden Hour Portrait').first()
        self.assertIsNotNone(p)
        self.assertEqual(p.original_prompt, 'A scenic golden hour portrait, 85mm lens')
        self.assertEqual(p.negative_prompt, 'blurry, dark')
        self.assertEqual(p.author, self.user)
        self.assertEqual(len(p.tags), 3)
        self.assertIn('85mm lens', [t.name for t in p.tags])

    def test_prompt_edit_permissions(self):
        p = PromptEntry(title='Original Title', original_prompt='original prompt', user_id=self.user.id)
        db.session.add(p)
        db.session.commit()

        # Login as other user
        self.login(username='other_director', password='password123')
        
        # Try to edit other user's prompt
        response = self.client.post(f'/prompt/{p.id}/edit', data={
            'title': 'Hacked Title',
            'original_prompt': 'hacked prompt',
            'tags': 'hack'
        })
        self.assertEqual(response.status_code, 403)
        
        # Try to delete other user's prompt
        response = self.client.post(f'/prompt/{p.id}/delete')
        self.assertEqual(response.status_code, 403)

    def test_prompt_edit_success(self):
        p = PromptEntry(title='Original Title', original_prompt='original prompt', user_id=self.user.id)
        db.session.add(p)
        db.session.commit()

        self.login()
        response = self.client.post(f'/prompt/{p.id}/edit', data={
            'title': 'Updated Title',
            'original_prompt': 'updated prompt content',
            'negative_prompt': 'no noise',
            'tags': 'new tag, edited'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        db.session.refresh(p)
        self.assertEqual(p.title, 'Updated Title')
        self.assertEqual(p.original_prompt, 'updated prompt content')
        self.assertEqual(len(p.tags), 2)

    def test_prompt_delete(self):
        p = PromptEntry(title='To Be Deleted', original_prompt='delete me', user_id=self.user.id)
        db.session.add(p)
        db.session.commit()

        self.login()
        response = self.client.post(f'/prompt/{p.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        deleted_prompt = PromptEntry.query.get(p.id)
        self.assertIsNone(deleted_prompt)

    def test_diary_crud_anonymous(self):
        response = self.client.get('/diary')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/diary/new')
        self.assertEqual(response.status_code, 302)

    def test_diary_creation_independent(self):
        self.login()
        response = self.client.post('/diary/new', data={
            'title': 'First Experiment',
            'content': 'Tested different light setups today.',
            'prompt_entry_id': -1
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        entry = AIDiaryEntry.query.filter_by(title='First Experiment').first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.content, 'Tested different light setups today.')
        self.assertIsNone(entry.prompt_entry_id)

    def test_diary_creation_linked(self):
        p = PromptEntry(title='Test Prompt', original_prompt='test', user_id=self.user.id)
        db.session.add(p)
        db.session.commit()

        self.login()
        response = self.client.post('/diary/new', data={
            'title': 'Linked Experiment',
            'content': 'Tested the linked prompt.',
            'prompt_entry_id': p.id
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        entry = AIDiaryEntry.query.filter_by(title='Linked Experiment').first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.prompt_entry_id, p.id)

    def test_diary_creation_linked_invalid_user(self):
        # Prompt owned by other_user
        p = PromptEntry(title='Other Prompt', original_prompt='other', user_id=self.other_user.id)
        db.session.add(p)
        db.session.commit()

        self.login()
        # Attempt to link to other user's prompt
        response = self.client.post('/diary/new', data={
            'title': 'Illegal Link',
            'content': 'Should fail verification.',
            'prompt_entry_id': p.id
        }, follow_redirects=True)

        # Triggers a form validation error on select choices
        html = response.data.decode('utf-8')
        self.assertIn('Not a valid choice.', html)
        
        # Verify diary entry was NOT created
        entry = AIDiaryEntry.query.filter_by(title='Illegal Link').first()
        self.assertIsNone(entry)

    def test_diary_edit_permissions(self):
        entry = AIDiaryEntry(title='Test Diary', content='content', user_id=self.user.id)
        db.session.add(entry)
        db.session.commit()

        self.login(username='other_director', password='password123')
        
        response = self.client.post(f'/diary/{entry.id}/edit', data={
            'title': 'Hacked Diary',
            'content': 'hacked content',
            'prompt_entry_id': -1
        })
        self.assertEqual(response.status_code, 403)

        response = self.client.post(f'/diary/{entry.id}/delete')
        self.assertEqual(response.status_code, 403)

    def test_diary_edit_success(self):
        entry = AIDiaryEntry(title='Original Diary', content='original content', user_id=self.user.id)
        db.session.add(entry)
        db.session.commit()

        self.login()
        response = self.client.post(f'/diary/{entry.id}/edit', data={
            'title': 'Updated Diary',
            'content': 'updated content',
            'prompt_entry_id': -1
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        db.session.refresh(entry)
        self.assertEqual(entry.title, 'Updated Diary')
        self.assertEqual(entry.content, 'updated content')

    def test_diary_delete(self):
        entry = AIDiaryEntry(title='To Be Deleted', content='delete', user_id=self.user.id)
        db.session.add(entry)
        db.session.commit()

        self.login()
        response = self.client.post(f'/diary/{entry.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        deleted_entry = AIDiaryEntry.query.get(entry.id)
        self.assertIsNone(deleted_entry)

    def test_create_prompt_new_route(self):
        self.login()
        response = self.client.post('/create', data={
            'title': 'Test Create Route',
            'original_prompt': 'A cinematic shot, 35mm lens, neon street lights',
            'negative_prompt': 'blurry, noise',
            'tags': '35mm, neon, cinematic'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        p = db.session.scalar(select(PromptEntry).where(PromptEntry.title == 'Test Create Route'))
        self.assertIsNotNone(p)
        self.assertEqual(p.original_prompt, 'A cinematic shot, 35mm lens, neon street lights')
        self.assertEqual(p.negative_prompt, 'blurry, noise')
        self.assertEqual(p.author, self.user)
        self.assertEqual(len(p.tags), 3)
        self.assertIn('35mm', [t.name for t in p.tags])
        self.assertIn('neon', [t.name for t in p.tags])
        self.assertIn('cinematic', [t.name for t in p.tags])

