from project import db

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref


class Receipt(db.Model):
    __tablename__ = 'receipt'

    id             = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    company_id     = db.Column(db.Integer,     nullable=False)
    emission_date  = db.Column(db.DateTime,    nullable=False)
    emission_place = db.Column(db.String(128), nullable=False)
    cnpj           = db.Column(db.String,      nullable=False)
    tax_value      = db.Column(db.Float,       nullable=False)
    total_price    = db.Column(db.Float,       nullable=False)
    title          = db.Column(db.String,      nullable=False)
    description    = db.Column(db.Text,        nullable=False)
    tag_id         = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=True)
    tags           = db.relationship('Tag', backref=db.backref('receipts', lazy=True))

    def __init__(self, company_id, emission_date, emission_place, cnpj, tax_value, total_price, title, description, tag_id):
        self.company_id     = company_id 
        self.emission_date  = emission_date 
        self.emission_place = emission_place
        self.cnpj           = cnpj
        self.tax_value      = tax_value 
        self.total_price    = total_price
        self.title          = title
        self.description    = description
        self.tag_id         = tag_id 

    def to_json(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'emission_date': self.emission_date.date().isoformat(),
            'emission_place': self.emission_place,
            'cnpj': self.cnpj,
            'tax_value': self.tax_value,
            'total_price': self.total_price,
            'title': self.title,
            'description': self.description,
            'tag_id': self.tag_id
        }


class Product(db.Model):
    __tablename__ = 'product'
    id         = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)
    receipt    = db.relationship('Receipt', backref=db.backref('products', lazy=True, cascade='all, delete-orphan'))
    quantity   = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    def __init__(self, receipt_id, quantity, unit_price):
        self.receipt_id = receipt_id
        self.quantity   = quantity
        self.unit_price = unit_price

    def to_json(self):
        return {
            'id':self.id,
            'receipt_id':self.receipt_id,
            'quantity':self.quantity,
            'unit_price':self.unit_price
        }

class Tag(db.Model):
    __tablename__ = 'tag'
    id         = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    company_id     = db.Column(db.Integer,     nullable=False)
    category   = db.Column(db.String(50), nullable=False)
    color      = db.Column(db.String(50), nullable=True)

    def __init__(self, category, company_id, color):
        self.category = category
        self.company_id = company_id
        self.color = color
    
    def to_json(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'category': self.category,
            'color': self.color
        } 