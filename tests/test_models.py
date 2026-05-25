import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, PromptEntry, Tag, AIDiaryEntry

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing_and_verification(self):
        u = User(username='test_user', email='user@example.com')
        u.set_password('password123')
        self.assertTrue(u.check_password('password123'))
        self.assertFalse(u.check_password('wrong_password'))
        self.assertNotEqual(u.password_hash, 'password123')

    def test_user_prompt_relationship(self):
        u = User(username='test_user', email='user@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        p = PromptEntry(
            title='test_title',
            original_prompt='test_original_prompt',
            negative_prompt='test_negative_prompt',
            user_id=u.id
        )
        db.session.add(p)
        db.session.commit()

        self.assertEqual(u.prompts.count(), 1)
        self.assertEqual(u.prompts.first().title, 'test_title')
        self.assertEqual(p.author, u)

    def test_prompt_tag_many_to_many_relationship(self):
        u = User(username='test_user', email='user@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        p1 = PromptEntry(
            title='prompt1',
            original_prompt='test_original_prompt_1',
            user_id=u.id
        )
        p2 = PromptEntry(
            title='prompt2',
            original_prompt='test_original_prompt_2',
            user_id=u.id
        )

        t1 = Tag(name='tag1')
        t2 = Tag(name='tag2')

        db.session.add_all([p1, p2, t1, t2])
        db.session.commit()

        # Link tag1 and tag2 to prompt1
        p1.tags.append(t1)
        p1.tags.append(t2)
        # Link tag1 to prompt2
        p2.tags.append(t1)

        db.session.commit()

        # Check prompt1 tags
        self.assertEqual(len(p1.tags), 2)
        self.assertIn(t1, p1.tags)
        self.assertIn(t2, p1.tags)

        # Check tag1 prompts (should be linked to both prompt1 and prompt2)
        self.assertEqual(len(t1.prompts), 2)
        self.assertIn(p1, t1.prompts)
        self.assertIn(p2, t1.prompts)

    def test_ai_diary_entry_relationships(self):
        u = User(username='test_user', email='user@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        p = PromptEntry(
            title='prompt1',
            original_prompt='test_original_prompt_1',
            user_id=u.id
        )
        db.session.add(p)
        db.session.commit()

        # Create diary entry linked to prompt
        d1 = AIDiaryEntry(
            title='diary1',
            content='diary_content_1',
            user_id=u.id,
            prompt_entry_id=p.id
        )
        # Create diary entry not linked to prompt (independent)
        d2 = AIDiaryEntry(
            title='diary2',
            content='diary_content_2',
            user_id=u.id,
            prompt_entry_id=None
        )
        db.session.add_all([d1, d2])
        db.session.commit()

        # Check User's diary entries
        self.assertEqual(u.diary_entries.count(), 2)
        self.assertIn(d1, u.diary_entries)
        self.assertIn(d2, u.diary_entries)

        # Check PromptEntry diary entries
        self.assertEqual(p.diary_entries.count(), 1)
        self.assertIn(d1, p.diary_entries)
        self.assertNotIn(d2, p.diary_entries)

        # Check diary entry properties
        self.assertEqual(d1.author, u)
        self.assertEqual(d1.prompt_entry, p)
        self.assertEqual(d2.author, u)
        self.assertIsNone(d2.prompt_entry)
