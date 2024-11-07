from flask import request, jsonify
from services.account import AccountService
from enums.transaction_enum import PaymentMethod

class TransactionController:
    @staticmethod
    def create_transaction():
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
