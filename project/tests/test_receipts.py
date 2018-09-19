import json
import unittest
from project.tests.base import BaseTestCase
from project.api.models import Receipt
from project import db


def add_receipt(company_id, emission_date, emission_place, tax_value, total_price):
    receipt = Receipt(company_id, emission_date, emission_place, tax_value, total_price)
    db.session.add(receipt)
    db.session.commit()
    return receipt

class TestReceiptservice(BaseTestCase):
    
    def test_receipts(self):
        response = self.client.get('/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Kalkuli Receipts Service!', data['data'])
    
    def test_get_all_receipts(self):


        
if __name__ == '__main__':
    unittest.main()