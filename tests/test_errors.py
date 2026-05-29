import unittest
from app import create_app, db

class ErrorsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404_error(self):
        response = self.client.get('/var-olmayan-sayfa-url')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Aradığınız sahne mevcut değil', response.data.decode('utf-8'))

    def test_500_error(self):
        self.app.config['PROPAGATE_EXCEPTIONS'] = False
        # Define a temporary route that raises an exception to trigger a 500 error
        @self.app.route('/trigger-500')
        def trigger_500():
            raise Exception('Kurgu Hatası Testi')

        response = self.client.get('/trigger-500')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Beklenmedik bir kurgu hatası oluştu', response.data.decode('utf-8'))
