import json
import unittest
from datetime import datetime
from project.tests.base import BaseTestCase
from project.api.models import Receipt
from project.api.models import Tag
from project import db



def add_receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price, title, description):
    receipt = Receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price, title, description)
    db.session.add(receipt)
    db.session.commit()
    return receipt

def add_tag(category):
    tag = Tag(category)
    db.session.add(tag)
    db.session.commit()
    return tag


class TestReceiptservice(BaseTestCase):
    def test_get_all_receipts(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande")
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description")

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
            self.assertIn('Geladeira', data['data']['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['data']['receipts'][0]['description'])

            self.assertEqual(16, data['data']['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['data']['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['data']['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['data']['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['data']['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['data']['receipts'][1]['total_price'])
            self.assertIn('Notebook', data['data']['receipts'][1]['title'])
            self.assertIn('Isso é outro description', data['data']['receipts'][1]['description'])

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
                        'title': 'Geladeira',
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

    def test_add_task_missing_cnpj(self):

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
        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, 'Geladeira', 'Geladeira Electrolux em 12x')

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
            self.assertIn('Geladeira', data['data']['title'])
            self.assertIn('Geladeira Electrolux em 12x', data['data']['description'])

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

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande")
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description")

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
            self.assertIn('00.000.000/0000-00', data['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['receipts'][0]['description'])

            self.assertEqual(16, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])
            self.assertIn('Notebook', data['receipts'][1]['title'])
            self.assertIn('Isso é outro description', data['receipts'][1]['description'])
            

    def test_filter_date_no_receipts(self):
        date_from = "22-07-1900"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()
        date_to = "22-09-1900"
        end = datetime.strptime(date_from, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande")
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description")

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

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande")
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description")


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
            self.assertIn('00.000.000/0000-00', data['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['receipts'][0]['description'])

            self.assertEqual(16, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])
            self.assertIn('Notebook', data['receipts'][1]['title'])
            self.assertIn('Isso é outro description', data['receipts'][1]['description'])


    def test_filter_date_missing_date_to(self):
        date_from = "22-07-2018"
        start = datetime.strptime(date_from, '%d-%m-%Y').date()

        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, "Geladeira", "Isso é uma descrição bem grande")
        add_receipt(16, date, "Gitlab", "00.000.000/0000-00", 15.0, 20.0, "Notebook", "Isso é outro description")


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
            self.assertIn('00.000.000/0000-00', data['receipts'][0]['cnpj'])
            self.assertEqual(20.0, data['receipts'][0]['tax_value'])
            self.assertEqual(50.0, data['receipts'][0]['total_price'])
            self.assertIn('Geladeira', data['receipts'][0]['title'])
            self.assertIn('Isso é uma descrição bem grande', data['receipts'][0]['description'])

            self.assertEqual(16, data['receipts'][1]['company_id'])
            self.assertEqual(date.isoformat(), data['receipts'][1]['emission_date'])
            self.assertIn('Gitlab', data['receipts'][1]['emission_place'])
            self.assertIn('00.000.000/0000-00', data['receipts'][1]['cnpj'])
            self.assertEqual(15.0, data['receipts'][1]['tax_value'])
            self.assertEqual(20.0, data['receipts'][1]['total_price'])
            self.assertIn('Notebook', data['receipts'][1]['title'])
            self.assertIn('Isso é outro description', data['receipts'][1]['description'])

    def test_remove_receipt(self):
        date_text = "22-09-2018"
        date = datetime.strptime(date_text, '%d-%m-%Y').date()

        receipt = add_receipt(15, date, "GitHub", "00.000.000/0000-00", 20.0, 50.0, 'Geladeira', 'Geladeira Electrolux em 12x')

        with self.client:
            response = self.client.delete(f'/receipt/{receipt.id}')
            data = json.loads(response.data.decode())
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Receipt deleted', data['data']['message'])

    def test_get_tags(self):
        add_tag('Alimentação')
        add_tag('Eletrodoméstico')

        with self.client:
            response = self.client.get('/tags')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['tags']), 2)

            self.assertIn('success', data['status'])

            self.assertIn('Alimentação', data['data']['tags'][0]['category'])

            self.assertIn('Eletrodoméstico', data['data']['tags'][1]['category'])
    
    def test_add_tag(self):
        with self.client:

            response = self.client.post(
                '/tag',
                data=json.dumps({
                    'tag': {
                        'category': 'Alimentação'
                    }
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('Tag was created', data['data']['message'])
            self.assertIn('success', data['status'])

if __name__ == '__main__':
    unittest.main()