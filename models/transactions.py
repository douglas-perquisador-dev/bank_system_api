from config import db
from enums import transaction_enum


class Transaction(db.Model):
    __tablename__ = 'transacao'
    id = db.Column(db.Integer, primary_key=True)
    numero_conta = db.Column(db.Integer, db.ForeignKey('conta.numero_conta'), nullable=False)
    forma_pagamento = db.Column(db.Enum(transaction_enum.PaymentMethod), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_transacao = db.Column(db.DateTime, nullable=False)
