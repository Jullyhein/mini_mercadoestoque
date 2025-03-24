from flask import Flask, request, jsonify
from twilio.rest import Client
import os
import dotenv
import random
from ..model import Seller, db 
from ...config.settings import Config


app = Flask(__name__)

dotenv.load_dotenv()

# ✅ Adicionando a URI do banco corretamente
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sellers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)

db.init_app(app)  # Inicializa o banco dentro do app Flask

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Verifica se o telefone já existe no banco de dados
    existing_seller = Seller.query.filter_by(phone=data['phone']).first()
    if existing_seller:
        return jsonify({"error": "Seller with this phone already exists."}), 400
    
    # Verifica se o vendedor com o mesmo email já existe
    existing_email = Seller.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({"error": "Seller with this email already exists."}), 400

    activation_code = str(random.randint(1000, 9999))
    new_seller = Seller(
        name=data['name'], cnpj=data['cnpj'], email=data['email'],
        phone=data['phone'], password=data['password'], activation_code=activation_code
    )
    db.session.add(new_seller)
    db.session.commit()
    
    send_activation_code(data['phone'], activation_code)
    return jsonify({"message": "Seller registered. Activation code sent."}), 201

def send_activation_code(phone, code):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f'Seu código de ativação: {code}',
        from_=TWILIO_WHATSAPP_NUMBER,  # Certifique-se de que está no formato 'whatsapp:+14155238886'
        to=f'whatsapp:{phone}'  # Garante que o número do destinatário também está correto
    )

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    seller = Seller.query.filter_by(phone=data['phone']).first()
    if seller and seller.activation_code == data['code']:
        seller.status = 'Ativo'
        seller.activation_code = None
        db.session.commit()
        return jsonify({"message": "Account activated."}), 200
    return jsonify({"error": "Invalid code."}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Criando tabelas no contexto do app
    app.run(debug=True)