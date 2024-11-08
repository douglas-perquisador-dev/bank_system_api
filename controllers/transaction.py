from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from services.account import AccountService
from enums.transaction_enum import PaymentMethod

class TransactionController:

    @staticmethod
    @jwt_required()
    @swag_from({
        'tags': ['Account'],
        'security': [{'Bearer': []}],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'numero_conta': {'type': 'integer', 'example': 12345},
                        'forma_pagamento': {'type': 'string', 'example': 'D'},
                        'valor': {'type': 'number', 'example': 100.0}
                    },
                    'required': ['numero_conta', 'forma_pagamento', 'valor']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Transação realizada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'numero_conta': {'type': 'integer'},
                        'saldo': {'type': 'number'}
                    }
                }
            },
            404: {'description': 'Erro nos parâmetros da transação ou método de pagamento inválido'}
        }
    })
    def create_transaction():
        """Criação de uma transação bancária"""
        data = request.get_json()
        account_number = data.get("numero_conta")
        payment_method_str = data.get("forma_pagamento")
        amount = data.get("valor")

        if not all([account_number, payment_method_str, amount]):
            return jsonify({"error": "Numero da conta, método de pagamento, e valor são necessários"}), 404

        try:
            payment_method = PaymentMethod(payment_method_str)
        except ValueError:
            return jsonify({"error": "Método de pagamento inválido"}), 404

        try:
            account = AccountService.process_transaction(account_number, payment_method, amount)
            return jsonify({"numero_conta": account.numero_conta, "saldo": account.saldo}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
