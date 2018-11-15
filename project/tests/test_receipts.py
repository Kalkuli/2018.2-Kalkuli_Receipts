import json
import unittest
from datetime import datetime
from project.tests.base import BaseTestCase
from project.api.models import Receipt
from project.api.models import Tag
from project import db
from project.tests.utils import add_receipt, add_tag


class TestReceiptservice(BaseTestCase):
    def test_get_all_receipts(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description", None)

        with self.client:
            response = self.client.get('/15/receipts')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['receipts']), 1)

            self.assertIn('success', data['status'])

            self.assertEqual(15, data['data']['receipts'][0]['company_id'])
            self.assertEqual(date.isoformat(), data['data']['receipts'][0]['emission_date'])
            self.assertIn('GitHub', data['data']['receipts'][0]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['data']['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['data']['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['data']['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['data']['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['data']['receipts'][0]['description'])
            self.assertEqual(None, data['data']['receipts'][0]['tag_id'])

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
                        'title': 'Geladeira',
                        'tag_id': None,
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_invalid_json(self):
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

    def test_add_receipt_missing_company_id(self):

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
                        'title': 'Geladeira',
                        'tag_id': None,
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_emission_date(self):
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
                        'tag_id': None,
                        'title': 'Geladeira',
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_emission_place(self):

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
                        'title': 'Geladeira',
                        'tag_id': None,
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_cnpj(self):

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
                        'title': 'Geladeira',
                        'tag_id': None,
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_cnpj(self):

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
                        'tax_value': '123.12',
                        'tag_id': None,
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

    def test_add_receipt_missing_tax_value(self):

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
                        'tag_id': None,
                        'title': 'Geladeira',
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_total_price(self):

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
                        'title': 'Geladeira',
                        'tag_id': None,
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_products(self):

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
                        'tag_id': None,
                        'total_price': '456.45',
                        'title': 'Geladeira',
                        'description': 'Geladeira Electrolux em 12x'
                    }
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_receipt_missing_quantity(self):

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
                        'tag_id': None,
                        'title': 'Geladeira',
                        'description': 'Geladeira Electrolux em 12x',
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

    def test_add_receipt_missing_unit_price(self):

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
                        'tag_id': None,
                        'title': 'Geladeira',
                        'description': 'Geladeira Electrolux em 12x',
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
        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, 'Geladeira', 'Geladeira Electrolux em 12x', None)

        with self.client:
            response = self.client.get(f'/15/receipt/{receipt.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])

            self.assertEqual(15, data['data']['company_id'])
            self.assertEqual(date.isoformat(), data['data']['emission_date'])
            self.assertIn('GitHub', data['data']['emission_place'])
            self.assertIn('00.000.000/0000-00', data['data']['cnpj'])
            self.assertEqual(20.0, data['data']['tax_value'])
            self.assertEqual(50.0, data['data']['total_price'])
            self.assertIn('Geladeira', data['data']['title'])
            self.assertIn('Geladeira Electrolux em 12x', data['data']['description'])
            self.assertEqual(None, data['data']['tag_id'])

    def test_get_single_receipt_no_id(self):
        with self.client:
            response = self.client.get('/2/receipt/noid')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Receipt not found', data['message'])

    def test_get_single_receipt_inexistent_id(self):
        with self.client:
            response = self.client.get('/1/receipt/100000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Receipt not found', data['message'])
    
    def test_get_single_receipt_no_companyid(self):
        with self.client:
            response = self.client.get('/noid/receipt/2')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Receipt not found', data['message'])

    def test_get_single_receipt_inexistent_id(self):
        with self.client:
            response = self.client.get('/1000000000/receipt/1')
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

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description", None)

        with self.client:

            response = self.client.post(
                '/15/select_date',
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
            self.assertIn('00.000.000/0000-00', data['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['receipts'][0]['description'])
            self.assertEqual(None, data['receipts'][0]['tag_id'])            

    def test_filter_date_no_receipts(self):
        date_from = "22-07-1900"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()
        date_to = "22-09-1900"
        end = datetime.strptime(date_from, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description", None)

        with self.client:

            response = self.client.post(
                '/15/select_date',
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

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)
        add_receipt(15, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description", None)


        with self.client:

            response = self.client.post(
                '/15/select_date',
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
            self.assertIn('00.000.000/0000-00', data['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['receipts'][0]['description'])
            self.assertEqual(None, data['receipts'][0]['tag_id'])

            self.assertEqual(15, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])
            self.assertIn('Notebook', data['receipts'][1]['title'])
            self.assertIn('Isso é outro description', data['receipts'][1]['description'])
            self.assertEqual(None, data['receipts'][1]['tag_id'])


    def test_filter_date_missing_date_to(self):
        date_from = "22-07-2018"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)
        add_receipt(15, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description", None)


        with self.client:

            response = self.client.post(
                '/15/select_date',
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
            self.assertIn('00.000.000/0000-00', data['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['receipts'][0]['description'])
            self.assertEqual(None, data['receipts'][0]['tag_id'])

            self.assertEqual(15, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])
            self.assertIn('Notebook', data['receipts'][1]['title'])
            self.assertIn('Isso é outro description', data['receipts'][1]['description'])
            self.assertEqual(None, data['receipts'][1]['tag_id'])

    def test_remove_receipt(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, 'Geladeira', 'Geladeira Electrolux em 12x', None)

        with self.client:
            response = self.client.delete(f'/15/receipt/{receipt.id}')
            data = json.loads(response.data.decode())
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Receipt deleted', data['data']['message'])

    def test_remove_receipt_not_found(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        receipt = add_receipt(16, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, 'Geladeira', 'Geladeira Electrolux em 12x', None)

        with self.client:
            response = self.client.delete(f'/15/receipt/{receipt.id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('Receipt not found', data['message'])

    def test_get_tags(self):
        add_tag('Alimentação', 15, "#874845")
        add_tag('Eletrodoméstico', 15, '#844155')

        with self.client:
            response = self.client.get('/15/tags')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['tags']), 2)

            self.assertIn('success', data['status'])

            self.assertIn('Alimentação', data['data']['tags'][0]['category'])
            self.assertIn('#874845', data['data']['tags'][0]['color'])

            self.assertIn('Eletrodoméstico', data['data']['tags'][1]['category'])
            self.assertIn('#844155', data['data']['tags'][1]['color'])

    def test_update_tag(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)

        add_tag('Alimentação', 15, '#844155')

        with self.client:
            response = self.client.patch(
                f'/15/update_tag/{receipt.id}',
                data = json.dumps({
                    'tag_id': 1
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('Tag updated!', data['data']['message'])
            self.assertIn('success', data['status'])

    def test_update_tag_not_found(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        receipt = add_receipt(16, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)

        add_tag('Alimentação', 15, '#844155')

        with self.client:
            response = self.client.patch(
                f'/15/update_tag/{receipt.id}',
                data = json.dumps({
                    'tag_id': 1
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertIn('Receipt not found', data['message'])
            self.assertIn('fail', data['status'])

    def test_detach_tag(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande", None)

        with self.client:
            response = self.client.patch(
                f'/15/update_tag/{receipt.id}',
                data = json.dumps({
                    'tag_id': None
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('Tag detached from a receipt!', data['data']['message'])
            self.assertIn('success', data['status'])

    def test_create_tag(self):
        with self.client:
            response = self.client.post(
                '/create_tag',
                data=json.dumps({
                    "tag": {
                        "color": "black",
                        "company_id": 15,
                        "category": "Utilitários"
                    }
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('Tag was created!', data['data']['message'])
            self.assertIn('success', data['status'])

    def test_fail_create_tag(self):
        with self.client:
            response = self.client.post(
                '/create_tag',
                data=json.dumps({}),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('wrong json', data['message'])
            self.assertIn('fail', data['status'])

    def test_category_already_exists_create_tag(self):

        add_tag('Utilitários', 15, 'black')
        with self.client:
            response = self.client.post(
                '/create_tag',
                data=json.dumps({
                    "tag": {
                        "color": "black",
                        "company_id": 15,
                        "category": "Utilitários"
                    }
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 409)
            self.assertIn('Tag já existente!', data['message'])
            self.assertIn('fail', data['status'])

    def test_missing_category_create_tag(self):
        with self.client:
            response = self.client.post(
                '/create_tag',
                data=json.dumps({
                    "tag": {
                        "color": "yellow"
                    }
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Não é possível adicionar uma categoria sem nome', data['message'])
            self.assertIn('fail', data['status'])

    def test_missing_color_create_tag(self):
        with self.client:
            response = self.client.post(
                '/create_tag',
                data=json.dumps({
                    "tag": {
                        "category": "Pipoca"
                    }
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Não é possível adicionar uma categoria sem cor', data['message'])
            self.assertIn('fail', data['status'])


if __name__ == '__main__':
    unittest.main()