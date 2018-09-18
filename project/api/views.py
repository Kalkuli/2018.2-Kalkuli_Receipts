from flask import request, jsonify, Blueprint

from sqlalchemy import exc 
from project.api.models import Receipt

from project import db


receipts_blueprint = Blueprint('receipt', __name__) 

@receipts_blueprint.route('/api/receipt', methods=['POST'])
def add_receipt():
    post_data = request.get_json()

    error_response = {
            'status': 'fail',
            'message': 'empty json'
    }

    if not post_data:
        return jsonify(error_response), 400

    company_id = post_data.get('company_id')
    emission_date = post_data.get('emission_date')
    emission_place = post_data.get('emission_place')
    tax_value = post_data.get('tax_value')
    total_price = post_data.get('total_price')
    
    try:
        db.session.add(Receipt(company_id, emission_date, emission_place, tax_value, total_price))
        db.session.commit()

        response = {
            'status': 'success',
            'data': {
                'message': 'Receipt was created!'
            }
        }
        return jsonify(response), 201
    except exc.IntegrityError   :
        db.session.rollback()
        print("eita giovanna")
        return jsonify(error_response), 400

#@receipts_blueprint.route('/api/receipt/<receipt_id>', methods=['GET'])
#def get_single_receipt
