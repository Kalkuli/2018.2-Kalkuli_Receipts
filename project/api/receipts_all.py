import os 
from flask import Flask, request, redirect, url_for, jsonify, Blueprint 
from sqlalchemy import exc
from project import app
from project import db
from project.api.models import Receipt

receipts_all_blueprint = Blueprint('receipts-all', __name__)

@receipts_all_blueprint.route('/receipts-all', methods=['GET'])
def get_all_receipts():
   response = {
        'status': 'success'
        'data': {
            'receipts-all': [receipt.to_json() for receipt in Receipt.query.all()]
        }
   }
   return jsonify(response), 200



    