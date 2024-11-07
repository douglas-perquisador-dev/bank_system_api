from flask import Flask
from controllers.account import AccountController
from controllers.transaction import TransactionController
from config import app

# Rotas para Contas
app.add_url_rule('/conta', view_func=AccountController.create_account, methods=['POST'])
app.add_url_rule('/conta', view_func=AccountController.get_account, methods=['GET'])

# Rotas para registerar transações com a conta
app.add_url_rule('/transacao', view_func=TransactionController.create_transaction, methods=['POST'])
