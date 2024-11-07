from flask import request, jsonify
from config import app
from services.account import AccountService
from enums.transaction_enum import PaymentMethod


@app.route('/conta', methods=['POST'])
def create_account():
    data = request.get_json()
    account_number: int = data['numero_conta']
    balance: float = data.get('saldo', 0.0)
    try:
        account = AccountService.create_account(account_number, balance)
        return jsonify({"numero_conta": account.numero_conta, "saldo": account.saldo}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route('/transacao', methods=['POST'])
def create_transaction():
    data = request.get_json()
    account_number: int = data['numero_conta']
    payment_method_str: str = data['forma_pagamento']
    amount: float = data['valor']

    try:
        payment_method = PaymentMethod(payment_method_str)
    except ValueError:
        return jsonify({"error": "Forma de pagamento inválida"}), 400

    try:
        account = AccountService.process_transaction(account_number, payment_method, amount)
        return jsonify({"numero_conta": account.numero_conta, "valor": account.saldo}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

