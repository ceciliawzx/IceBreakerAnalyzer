# test_app.py
import unittest
import json
from flask_app import app  # Import your Flask app here
from test_data import users as sample_users_data


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_generate_reports(self):
        # Sample data to send for testing

        response = self.app.post('/generate_reports',
                                 data=json.dumps(sample_users_data),
                                 content_type='application/json')

        print(response.json)
        self.assertEqual(response.status_code, 200)
        # Assert more conditions based on your expected response structure


if __name__ == '__main__':
    unittest.main()
