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
        date_text = "22/09/2018"
        date = datetime.datetime.strptime(date_text, '%d/%m/%Y').date() 

        add_receipt(15, date, "GitHub", 20.0, 50.0)
        add_receipt(16, "20/10/2018", "Gitlab", 15.0, 20.0)

        with self.client:
            response = self.client.get('/receipt')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['receipt']), 2)

            self.assertIn('success', data['status'])

            self.assertIn(15, data['data']['receipt'][0]['company_id'])
            self.assertIn(date, data['data']['receipt'][0]['emission_date'])
            self.assertIn('Github', data['data']['receipt'][0]['emission_place'])
            self.assertIn(20.0, data['data']['receipt'][0]['tax_value'])
            self.assertIn(50.0, data['data']['receipt'][0]['total_price'])

            self.assertIn(16, data['data']['receipt'][1]['company_id'])
            self.assertIn(date, data['data']['receipt'][1]['emission_date'])
            self.assertIn('Gitlab', data['data']['receipt'][1]['emission_place'])
            self.assertIn(15.0, data['data']['receipt'][1]['tax_value'])
            self.assertIn(20.0, data['data']['receipt'][1]['total_price'])

                  
if __name__ == '__main__':
    unittest.main()