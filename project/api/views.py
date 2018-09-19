from flask import request, jsonify, Blueprint

from sqlalchemy import exc 
from project.api.models import Receipt
from project.api.models import Product

from project import db

receipts_blueprint = Blueprint('receipt', __name__) 

@receipts_blueprint.route('/receipt', methods=['GET'])
def get_all_receipts():
    response = {
        'status': 'success',
        'data': {
            'receipt': [receipt.json() for receipt in Receipt.query.all()]
        }
    } 
    return jsonify(response), 200
 

@receipts_blueprint.route('/receipt', methods=['POST'])
def add_receipt():
    post_data = request.get_json()
    print(post_data)

    error_response = {
            'status': 'fail',
            'message': 'wrong json'
    }

    if not post_data:
        return jsonify(error_response), 400

    company_id = post_data['receipt']['company_id']
    emission_date = post_data['receipt']['emission_date']
    emission_place = post_data['receipt']['emission_place']
    tax_value = post_data['receipt']['tax_value']
    total_price = post_data['receipt']['total_price']

    products = post_data['receipt']['products']
    
    try:
        receipt = Receipt(company_id, emission_date, emission_place, tax_value, total_price)
        db.session.add(receipt)
        db.session.flush()

        for product in products:
             db.session.add(Product(receipt.id, product['quantity'], product['unit_price']))

        db.session.commit()

        response = {
            'status': 'success',
            'data': {
                'message': 'Receipt was created!'
            }
        }
        return jsonify(response), 201
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(error_response), 400
