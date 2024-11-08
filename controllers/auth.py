from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from flasgger import swag_from
from models.users import User


class AuthController:

    @staticmethod
    @swag_from({
        'tags': ['Authentication'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string', 'example': 'user123'},
                        'password': {'type': 'string', 'example': 'password123'}
                    },
                    'required': ['username', 'password']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Login realizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'access_token': {'type': 'string', 'example': 'your_jwt_token'}
                    }
                }
            },
            401: {'description': 'Credenciais inválidas'}
        }
    })
    def login():
        """Autenticação de usuário com JWT"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401
