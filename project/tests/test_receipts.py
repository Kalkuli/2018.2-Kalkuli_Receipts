import json
import unittest
from datetime import datetime
from project.tests.base import BaseTestCase
from project.api.models import Receipt
from project import db


def add_receipt(company_id, emission_date, emission_place, tax_value, total_price):
    receipt = Receipt(company_id, emission_date, emission_place, tax_value, total_price)
    db.session.add(receipt)
    db.session.commit()
    return receipt

class TestReceiptservice(BaseTestCase):
    def test_get_all_receipts(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date() 

        add_receipt(15, date, "GitHub", 20.0, 50.0)
        add_receipt(16, date, "Gitlab", 15.0, 20.0)

        with self.client:
            response = self.client.get('/receipt')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['receipt']), 2)

            self.assertIn('success', data['status'])

            self.assertEqual(15, data['data']['receipt'][0]['company_id'])
            self.assertEqual(date, data['data']['receipt'][0]['emission_date'])
            self.assertIn('Github', data['data']['receipt'][0]['emission_place'])
            self.assertEqual(20.0, data['data']['receipt'][0]['tax_value'])
            self.assertEqual(50.0, data['data']['receipt'][0]['total_price'])

            self.assertEqual(16, data['data']['receipt'][1]['company_id'])
            self.assertEqual(date, data['data']['receipt'][1]['emission_date'])
            self.assertIn('Gitlab', data['data']['receipt'][1]['emission_place'])
            self.assertEqual(15.0, data['data']['receipt'][1]['tax_value'])
            self.assertEqual(20.0, data['data']['receipt'][1]['total_price'])

                  
if __name__ == '__main__':
    unittest.main()