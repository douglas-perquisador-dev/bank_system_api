from config import app
from flask import Flask
from controllers.account import AccountController
from controllers.transaction import TransactionController
from controllers.auth import AuthController
from flask_jwt_extended import jwt_required

# Rota para A
app.add_url_rule('/login', view_func=AuthController.login, methods=['POST'])
# Rotas para Contas
app.add_url_rule('/conta', view_func=jwt_required()(AccountController.create_account), methods=['POST'])
app.add_url_rule('/conta', view_func=jwt_required()(AccountController.get_account), methods=['GET'])

# Rotas para registerar transações com a conta
app.add_url_rule('/transacao', view_func=jwt_required()(TransactionController.create_transaction), methods=['POST'])
