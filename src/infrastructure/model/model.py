from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

#Agora db pode ser inicializado em qualquer parte do código sem precisar recriar o app.
db = SQLAlchemy()

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default='Inativo')
    activation_code = db.Column(db.String(4), nullable=True)