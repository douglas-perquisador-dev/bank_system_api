from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models.users import User


class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401