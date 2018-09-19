import json
import unittest
from project.tests.base import BaseTestCase


class TestReceiptservice(BaseTestCase):
    
    def test_receipts(self):
        response = self.client.get('/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Kalkuli Receipts Service!', data['data'])


        
if __name__ == '__main__':
    unittest.main()