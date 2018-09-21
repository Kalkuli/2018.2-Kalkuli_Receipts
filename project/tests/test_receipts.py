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
            response = self.client.get('/receipts')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['receipt']), 2)

            self.assertIn('success', data['status'])

            self.assertEqual(15, data['data']['receipt'][0]['company_id'])
            self.assertEqual(date.isoformat(), data['data']['receipt'][0]['emission_date'])
            self.assertIn('GitHub', data['data']['receipt'][0]['emission_place'])
            self.assertEqual(20.0, data['data']['receipt'][0]['tax_value'])
            self.assertEqual(50.0, data['data']['receipt'][0]['total_price'])

            self.assertEqual(16, data['data']['receipt'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['data']['receipt'][1]['emission_date'])
            self.assertIn('Gitlab', data['data']['receipt'][1]['emission_place'])
            self.assertEqual(15.0, data['data']['receipt'][1]['tax_value'])
            self.assertEqual(20.0, data['data']['receipt'][1]['total_price'])

    def test_add_receipt(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:

            response = self.client.post(
                '/receipt', 
                data = json.dumps({
                      'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products':[
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('Receipt was created!', data['data']['message'])
            self.assertIn('success', data['status'])

    def test_add_task_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({}),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_company_id(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products':[
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_emission_date(self):
        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products':[
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_emission_place(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products':[
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_tax_value(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'total_price': '456.45',
                        'products':[
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_total_price(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'products':[
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])
            

    def test_add_task_missing_products(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'total_price': '456.45'
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_quantity(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products':[
                            { 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])


    def test_add_task_missing_unit_price(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:
            response = self.client.post(
                '/receipt',
                data = json.dumps({
                    'receipt':{
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products':[
                            {'quantity': 1},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == '__main__':
    unittest.main()
