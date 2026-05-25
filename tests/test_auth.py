import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Kayıt Ol', html)

    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'director_x',
            'email': 'director@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        u = User.query.filter_by(username='director_x').first()
        self.assertIsNotNone(u)
        self.assertEqual(u.email, 'director@example.com')
        self.assertTrue(u.check_password('password123'))
        
        html = response.data.decode('utf-8')
        self.assertIn('Başarıyla kayıt oldunuz', html)

    def test_register_duplicate_username(self):
        u = User(username='director_x', email='director@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post('/auth/register', data={
            'username': 'director_x',
            'email': 'another@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Bu kullanıcı adı zaten alınmış', html)

    def test_register_duplicate_email(self):
        u = User(username='director_x', email='director@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()
        
        response = self.client.post('/auth/register', data={
            'username': 'another_director',
            'email': 'director@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Bu e-posta adresi zaten kayıtlı', html)

    def test_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Giriş Yap', html)

    def test_login_success_username(self):
        u = User(username='director_x', email='director@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/login', data={
            'username_or_email': 'director_x',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Başarıyla giriş yaptınız', html)
        self.assertIn('Çıkış Yap', html)

    def test_login_success_email(self):
        u = User(username='director_x', email='director@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/login', data={
            'username_or_email': 'director@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Başarıyla giriş yaptınız', html)

    def test_login_failure(self):
        u = User(username='director_x', email='director@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/login', data={
            'username_or_email': 'director_x',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Geçersiz kullanıcı adı', html)

    def test_logout_logged_in(self):
        u = User(username='director_x', email='director@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

        self.client.post('/auth/login', data={
            'username_or_email': 'director_x',
            'password': 'password123'
        })
        
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Başarıyla çıkış yaptınız', html)
        self.assertIn('Giriş Yap', html)

    def test_logout_anonymous(self):
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Giriş Yap', html)
