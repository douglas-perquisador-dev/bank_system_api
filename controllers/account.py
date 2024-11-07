from flask import request, jsonify
from services.account import AccountService


class AccountController:
    @staticmethod
    def create_account():
        data = request.get_json()
        account_number = data.get("numero_conta")
        balance = data.get("saldo", 0.0)

        if account_number is None:
            return jsonify({"error": "Numero da conta é necessário!"}), 404

        try:
            account = AccountService.create_account(account_number, balance)
            return jsonify({"account_number": account.numero_conta, "balance": account.saldo}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def get_account():
        try:
            account_number = request.args.get("numero_conta", type=int)

            if account_number is None:
                return jsonify({"error": "Um numero de conta é necessário."})

            account = AccountService.get_account(account_number)
            if account:
                return jsonify({"numero_conta": account.numero_conta, "saldo": account.saldo}), 201
            else:
                return jsonify({"error": "Conta não existente!"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
