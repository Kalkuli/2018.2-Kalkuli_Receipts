from project import db
from project.api.models import Receipt, Tag, Product

def add_receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price, title, description, tag_id):
    receipt = Receipt(company_id, emission_date, emission_place, cnpj, tax_value, total_price, title, description, tag_id)
    db.session.add(receipt)
    db.session.commit()
    return receipt

def add_tag(category, company_id, color):
    tag = Tag(category, company_id, color)
    db.session.add(tag)
    db.session.commit()
    return tag