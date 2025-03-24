import random
from sqlite3 import IntegrityError
from infrastructure.model.model import db, Seller

class SellerService:
    @staticmethod
    def register_seller(data):
        # Verifica se o vendedor com o mesmo email já existe
        existing_seller = Seller.query.filter_by(email=data['email']).first()
        if existing_seller:
            return {"error": "Seller with this email already exists."}, 400
        
        # Verifica se o vendedor com o mesmo telefone já existe
        existing_phone = Seller.query.filter_by(phone=data['phone']).first()
        if existing_phone:
            return {"error": "Seller with this phone already exists."}, 400

        # Cria o novo vendedor
        new_seller = Seller(
            name=data['name'], 
            cnpj=data['cnpj'], 
            email=data['email'],
            phone=data['phone'], 
            password=data['password'], 
            activation_code=str(random.randint(1000, 9999))
        )

        try:
            # Tenta adicionar e salvar no banco de dados
            db.session.add(new_seller)
            db.session.commit()
            return {"message": "Seller registered. Activation code sent."}, 201
        
        except IntegrityError as e:
            # Se ocorrer um erro de integridade, desfaz a transação
            db.session.rollback()
            return {"error": "Phone number already exists in the system."}, 400
