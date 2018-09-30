import json
import unittest
from datetime import datetime
from project.tests.base import BaseTestCase
from project.api.models import Receipt
from project import db



def add_receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price):
    receipt = Receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price)
    db.session.add(receipt)
    db.session.commit()
    return receipt


class TestReceiptservice(BaseTestCase):
    def test_get_all_receipts(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0)
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0)

        with self.client:
            response = self.client.get('/receipts')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['receipts']), 2)

            self.assertIn('success', data['status'])

            self.assertEqual(15, data['data']['receipts'][0]['company_id'])
            self.assertEqual(date.isoformat(), data['data']['receipts'][0]['emission_date'])
            self.assertIn('GitHub', data['data']['receipts'][0]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['data']['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['data']['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['data']['receipts'][0]['total_price'])

            self.assertEqual(16, data['data']['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['data']['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['data']['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['data']['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['data']['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['data']['receipts'][1]['total_price'])

    def test_add_receipt(self):

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        with self.client:

            response = self.client.post(
                '/receipt',
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products': [
                            {'quantity': 2, 'unit_price': 13.12},
                            {'quantity': 1, 'unit_price': 12.13}
                        ]
                    }
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('Receipt was created!', data['data']['message'])
            self.assertIn('success', data['status'])

    def test_add_task_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/receipt',
                data=json.dumps({}),
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
                data=json.dumps({
                    'receipt': {
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products': [
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products': [
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'cnpj': '00.000.000/0000-00',
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

    def test_add_task_missing_cnpj(self):

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
                content_type='application/json',
            )
            
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_task_missing_cnpj(self):

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
                        'cnpj': '00.000.000/0000-00',
                        'total_price': '456.45',
                        'products': [
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'total_price': '456.45',
                        'products': [
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'tax_value': '123.12',
                        'products': [
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products': [
                            {'unit_price': 13.12},
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
                data=json.dumps({
                    'receipt': {
                        'company_id': '1234',
                        'emission_date': date.isoformat(),
                        'emission_place': 'place',
                        'cnpj': '00.000.000/0000-00',
                        'tax_value': '123.12',
                        'total_price': '456.45',
                        'products': [
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

    def test_get_single_receipt(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date() 
        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0)

        with self.client:
            response = self.client.get(f'/receipt/{receipt.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])

            self.assertEqual(15, data['data']['company_id'])
            self.assertEqual(date.isoformat(), data['data']['emission_date'])
            self.assertIn('GitHub', data['data']['emission_place'])
            self.assertIn('00.000.000/0000-00', data['data']['cnpj'])
            self.assertEqual(20.0, data['data']['tax_value'])
            self.assertEqual(50.0, data['data']['total_price'])

    def test_get_single_receipt_no_id(self):
        with self.client:
            response = self.client.get('/receipt/noid')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Receipt not found', data['message'])

    def test_get_single_receipt_inexistent_id(self):
        with self.client:
            response = self.client.get('/receipt/100000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Receipt not found', data['message'])

    def test_filter_date(self):

        date_from = "22-07-2018"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()
        date_to = "22-10-2018"
        end = datetime.strptime(date_to, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0)
        add_receipt(16, date, "Gitlab","00.000.000/0000-00", 15.0, 20.0)


        with self.client:

            response = self.client.post(
                '/select_date',
                data = json.dumps({
                    "period": {
                        "date_from": start.isoformat(),
                        "date_to": end.isoformat()
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)

            self.assertEqual(15, data['receipts'][0]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][0]['emission_date'])
            self.assertIn('GitHub', data['receipts'][0]['emission_place'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])

            self.assertEqual(16, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])
            

    def test_filter_date_no_receipts(self):
        date_from = "22-07-1900"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()
        date_to = "22-09-1900"
        end = datetime.strptime(date_from, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub","00.000.000/0000-00", 20.0, 50.0)
        add_receipt(16, date, "Gitlab","00.000.000/0000-00", 15.0, 20.0)

        with self.client:

            response = self.client.post(
                '/select_date',
                data = json.dumps({
                    "period": {
                        "date_from": start.isoformat(),
                        "date_to": end.isoformat()
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('no receipts', data['empty'])

    def test_filter_date_missing_date_from(self):
        date_to = "22-10-2018"
        end = datetime.strptime(date_to, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub","00.000.000/0000-00", 20.0, 50.0)
        add_receipt(16, date, "Gitlab","00.000.000/0000-00", 15.0, 20.0)


        with self.client:

            response = self.client.post(
                '/select_date',
                data = json.dumps({
                    "period": {
                        "date_to": end.isoformat()
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)

            self.assertEqual(15, data['receipts'][0]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][0]['emission_date'])
            self.assertIn('GitHub', data['receipts'][0]['emission_place'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])

            self.assertEqual(16, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])


    def test_filter_date_missing_date_to(self):
        date_from = "22-07-2018"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub","00.000.000/0000-00", 20.0, 50.0)
        add_receipt(16, date, "Gitlab","00.000.000/0000-00", 15.0, 20.0)


        with self.client:

            response = self.client.post(
                '/select_date',
                data = json.dumps({
                    "period": {
                        "date_from": start.isoformat()
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)

            self.assertEqual(15, data['receipts'][0]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][0]['emission_date'])
            self.assertIn('GitHub', data['receipts'][0]['emission_place'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])

            self.assertEqual(16, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])

if __name__ == '__main__':
    unittest.main()
