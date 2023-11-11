from app import app
from unittest import TestCase

class QRCoderTestCase(TestCase):
    def test_register(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Register Here:</h2>', html)
            
    def test_login(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Login Here:</h2>', html)
    

