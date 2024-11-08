from flask import request, jsonify
from flasgger import swag_from
from services.account import AccountService
from flask_jwt_extended import jwt_required

class AccountController:

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
                        'saldo': {'type': 'number', 'example': 100.0}
                    },
                    'required': ['numero_conta']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Conta criada com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'numero_conta': {'type': 'integer'},
                        'saldo': {'type': 'number'}
                    }
                }
            },
            404: {'description': 'Numero da conta é necessário!'}
        }
    })
    def create_account():
        """Criação de uma nova conta"""
        data = request.get_json()
        account_number = data.get("numero_conta")
        balance = data.get("saldo", 0.0)

        if account_number is None:
            return jsonify({"error": "Numero da conta é necessário!"}), 404

        try:
            account = AccountService.create_account(account_number, balance)
            return jsonify({"numero_conta": account.numero_conta, "saldo": account.saldo}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    @jwt_required()
    @swag_from({
        'tags': ['Account'],
        'security': [{'Bearer': []}],
        'parameters': [
            {
                'name': 'numero_conta',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'Número da conta bancária'
            }
        ],
        'responses': {
            200: {
                'description': 'Informações da conta',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'numero_conta': {'type': 'integer'},
                        'saldo': {'type': 'number'}
                    }
                }
            },
            404: {'description': 'Conta não existente ou número da conta é necessário.'}
        }
    })
    def get_account():
        """Obtenção de uma conta existente"""
        try:
            account_number = request.args.get("numero_conta", type=int)

            if account_number is None:
                return jsonify({"error": "Um numero de conta é necessário."})

            account = AccountService.get_account(account_number)
            if account:
                return jsonify({"numero_conta": account.numero_conta, "saldo": account.saldo}), 200
            else:
                return jsonify({"error": "Conta não existente!"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
