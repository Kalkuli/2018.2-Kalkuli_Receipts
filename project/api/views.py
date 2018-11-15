import datetime
from flask import request, jsonify, Blueprint

from sqlalchemy import exc
from project.api.models import Receipt
from project.api.models import Product
from project.api.models import Tag

from project import db

receipts_blueprint = Blueprint('receipt', __name__)


@receipts_blueprint.route('/<company_id>/receipts', methods=['GET'])
def get_all_receipts(company_id):
    response = {
        'status': 'success',
        'data': {
            'receipts': [receipt.to_json() for receipt in Receipt.query.filter_by(company_id=int(company_id))]
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
    title = receipt.get('title')
    description = receipt.get('description')
    tag_id = receipt.get('tag_id')

    products = receipt.get('products')

    if products is None:
        return jsonify(error_response), 400

    try:
        receipt = Receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price, title, description, tag_id)
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



@receipts_blueprint.route('/<company_id>/receipt/<receipt_id>', methods=['GET'])
def get_single_receipt(company_id, receipt_id):
    error_response = {
        'status': 'fail',
        'message': 'Receipt not found'
    }
    try:
        receipt = Receipt.query.filter_by(id=int(receipt_id), company_id=int(company_id)).first()

        if not receipt:
            return jsonify(error_response), 404

        response = {
            'status': 'success',
            'data': receipt.to_json()
        }
    except ValueError:
        return jsonify(error_response), 404

    return jsonify(response), 200

@receipts_blueprint.route('/<company_id>/select_date', methods=['POST'])
def filter_date(company_id):
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
        'receipts': [receipt.to_json() for receipt in Receipt.query.filter(Receipt.emission_date <= end).filter(Receipt.emission_date >= start).filter(Receipt.company_id == int(company_id))]
    }

    if not response.get('receipts'):
        return jsonify({
            'empty': 'no receipts'
        }), 400

    return jsonify(response), 200
    
@receipts_blueprint.route('/<company_id>/receipt/<receipt_id>', methods=['DELETE'])
def delete_receipt(company_id, receipt_id):
    error_response = {
        'status': 'fail',
        'message': 'Receipt not found'
    }

    receipt = Receipt.query.filter_by(id=int(receipt_id), company_id=int(company_id)).first()

    if not receipt:
        return jsonify(error_response), 404

    db.session.delete(receipt)
    db.session.commit()

    response = {
        'status': 'success',
        'data': {
            'message': 'Receipt deleted'
        }
    }

    return jsonify(response), 200


@receipts_blueprint.route('/tags', methods=['GET'])
def get_all_tags(): 
    response = {
        'status': 'success',
        'data': {
            'tags': [tag.to_json() for tag in Tag.query.all()]
        }
    }
    return jsonify(response), 200

@receipts_blueprint.route('/<company_id>/update_tag/<receipt_id>', methods=['PATCH'])
def update_tag(company_id, receipt_id):
    post_data = request.get_json()

    tag_id = post_data.get('tag_id')

    receipt = Receipt.query.filter_by(id=int(receipt_id), company_id=int(company_id)).first()
    if not receipt:
        error_response = {
            'status': 'fail',
            'message': 'Receipt not found'
        }
        return jsonify(error_response), 404


    receipt.tag_id = tag_id
    db.session.commit()

    if receipt.tag_id is None:
        response = {
            'status': 'success',
            'data': {
                'message': 'Tag detached from a receipt!'
            }
        }
    else:
        response = {
            'status': 'success',
            'data': {
                'message': 'Tag updated!'
            }
        }
    
    return jsonify(response), 200

@receipts_blueprint.route('/create_tag', methods=['POST'])
def create_tag():
    post_data = request.get_json()

    error_response = {
        'status': 'fail',
        'message': 'wrong json'
    }

    error_response_missing_category = {
        'status': 'fail',
        'message': 'Não é possível adicionar uma categoria sem nome'
    }

    error_response_missing_color = {
        'status': 'fail',
        'message': 'Não é possível adicionar uma categoria sem cor'
    }

    if not post_data:
        return jsonify(error_response), 400

    tag = post_data.get('tag')

    category = tag.get('category')

    if not category:
        return jsonify(error_response_missing_category), 400

    color = tag.get('color')

    if not color:
        return jsonify(error_response_missing_color), 400

    check_tag = []
    for check_tag in Tag.query.all():
        if category == check_tag.to_json().get('category'):
            return jsonify({
                'status': 'fail',
                'message': 'Tag já existente!'
            }), 409

    try:
        tag = Tag(category, color)
        db.session.add(tag)
        db.session.commit()

        response = {
            'status': 'success',
            'data': {
                'message': 'Tag was created!'
            }
        }

        return jsonify(response), 201

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(error_response), 400