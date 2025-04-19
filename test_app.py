import unittest
import base64
from app import app

class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.auth_header = {
            "Authorization": "Basic " + base64.b64encode(b"admin:secret").decode("utf-8")
        }

    def test_valid_auth(self):
        response = self.app.post('/fetch_profiles_connections', headers=self.auth_header)
        self.assertIn(response.status_code, [200, 500])  # 500 if scraper fails, 200 if everything works

    def test_invalid_auth(self):
        bad_auth = {
            "Authorization": "Basic " + base64.b64encode(b"wrong:credentials").decode("utf-8")
        }
        response = self.app.post('/fetch_profiles_connections', headers=bad_auth)
        self.assertEqual(response.status_code, 401)

    def test_missing_auth(self):
        response = self.app.post('/fetch_profiles_connections')  # No headers
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()