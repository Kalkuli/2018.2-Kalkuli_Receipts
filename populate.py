from project.api.models import Receipt, Product, Tag

def seedTags(db):
    db.session.add(Tag(category='Transporte',  company_id=1, color='#79B473'))
    db.session.add(Tag(category='Alimentação', company_id=2, color='#DB5461'))
    db.session.add(Tag(category='Eletrônicos', company_id=3, color='#593C8F'))
    db.session.add(Tag(category='Limpeza',     company_id=3, color='#5CC8FF'))
    db.session.commit()

# Creates Receipts
def seedReceipts(db):
    db.session.add(Receipt(company_id=1, emission_date='2018-01-01', 
                    emission_place='Terminal BRT Gama', cnpj='123456', tax_value='12.40', 
                    total_price=120.50, title='Passe', description='Passe Estudantil', tag_id=1))
    db.session.add(Receipt(company_id=2, emission_date='2018-01-01', 
                    emission_place='Shopping do Gama', cnpj='123456', tax_value='12.40', 
                    total_price=42.80, title='Almoço', description='Macarrão', tag_id=2))
    db.session.add(Receipt(company_id=3, emission_date='2018-01-01', 
                    emission_place='Apple', cnpj='123456', tax_value='12.40', 
                    total_price=9999.99, title='Compra Superfaturada', description='AIpode!', tag_id=3))
    db.session.commit()
