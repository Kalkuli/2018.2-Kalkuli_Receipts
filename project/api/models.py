from project import db

from sqlalchemy.sql import func


class Receipt(db.Model):
    __tablename__ = 'receipt'

    id             = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    company_id     = db.Column(db.Integer,  nullable=False)
    emission_date  = db.Column(db.String, nullable=False)
    emission_place = db.Column(db.String(128), nullable=False)
    tax_value      = db.Column(db.Float,    nullable=False)
    total_price    = db.Column(db.Float,    nullable=False)
    tagUseReports  = db.relationship('product',   backref='receipt', lazy=True)

    def __init__(self, company_id, emission_date, emission_place, tax_value, total_price):
        self.company_id     = company_id 
        self.emission_date  = emission_date 
        self.emission_place = emission_place 
        self.tax_value      = tax_value 
        self.total_price    = total_price 

    def to_json(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'emission_date': self.emission_date,
            'emission_place': self.emission_place,
            'tax_value': self.tax_value,
            'total_price': self.total_price
        }


class Product(db.Model):
    __tablename__ = 'product'
    id         = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    def __init__(self, receipt_id, quantity, unit_price):
        self.receipt_id = receipt_id
        self.quantity   = quantity
        self.unit_price = unit_price
