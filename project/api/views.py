import datetime
from flask import request, jsonify, Blueprint

from sqlalchemy import exc
from project.api.models import Receipt
from project.api.models import Product

from project import db

receipts_blueprint = Blueprint('receipt', __name__)


@receipts_blueprint.route('/receipts', methods=['GET'])
def get_all_receipts():
    response = {
        'status': 'success',
        'data': {
            'receipts': [receipt.to_json() for receipt in Receipt.query.all()]
        }
    }
    return jsonify(response), 200


@receipts_blueprint.route('/receipt', methods=['POST'])
def add_receipt():
    post_data = request.get_json()

    error_response = {
        'status': 'fail',
        'message': 'wrong json'
    }

    if not post_data:
        return jsonify(error_response), 400

    receipt = post_data.get('receipt')

    company_id = receipt.get('company_id')
    emission_date = receipt.get('emission_date')
    emission_place = receipt.get('emission_place')
    cnpj = receipt.get('cnpj')
    tax_value = receipt.get('tax_value')
    total_price = receipt.get('total_price')

    products = receipt.get('products')

    if products is None:
        return jsonify(error_response), 400

    try:
        receipt = Receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price)
        db.session.add(receipt)
        db.session.flush()

        for product in products:
            db.session.add(Product(receipt.id, product.get(
                'quantity'), product.get('unit_price')))

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



@receipts_blueprint.route('/receipt/<receipt_id>', methods=['GET'])
def get_single_receipt(receipt_id):
    error_response = {
        'status': 'fail',
        'message': 'Receipt not found'
    }
    try:
        receipt = Receipt.query.filter_by(id=int(receipt_id)).first()

        if not receipt:
            return jsonify(error_response), 404

        response = {
            'status': 'success',
            'data': receipt.to_json()
        }
    except ValueError:
        return jsonify(error_response), 404

    return jsonify(response), 200

@receipts_blueprint.route('/select_date', methods=['POST'])
def filter_date():
    post_data_date = request.get_json()

    error_response = {
        'status': 'fail',
        'message': 'wrong json'
    }

    date = post_data_date.get('period')

    date_from = date.get('date_from')
    date_to = date.get('date_to')

    if not date_from:
        date_from = "1900-01-01"
    
    if not date_to:
        date_to = "3000-12-30"  

    start = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
    end = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()

    
    response = {
        'receipts': [receipt.to_json() for receipt in Receipt.query.filter(Receipt.emission_date <= end).filter(Receipt.emission_date >= start)]
    }

    if not response.get('receipts'):
        return jsonify({
            'empty': 'no receipts'
        }), 400

    return jsonify(response), 200
    
@receipts_blueprint.route('/receipt/<receipt_id>', methods=['DELETE'])
def delete_receipt(receipt_id):
    error_response = {
        'status': 'fail',
        'message': 'Receipt not found'
    }
    try:
        receipt = Receipt.query.filter_by(id=int(receipt_id)).first()
        db.session.delete(receipt)
        db.session.commit()

        response = {
            'status': 'success',
            'data': {
                'message': 'Receipt deleted'
            }
        }

    except ValueError:
        return jsonify(error_response), 404

    return jsonify(response), 200