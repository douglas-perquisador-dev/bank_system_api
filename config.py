import os
import secrets
from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

load_dotenv()
# initiating Flask
app = Flask(__name__)

# Config BD (RDS PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://objective:123456@postgres:5432/bank_system')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # todas as rotas são documentadas
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header usando o formato Bearer. Exemplo: \"Authorization: Bearer {token}\""
        }
    },
    "security": [{"Bearer": []}],
}
swagger = Swagger(app, template={
    "info": {
        "title": "Bank System API",
        "description": "Documentação da API do sistema de gestão bancária",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/"
}, config=swagger_config)


# Config JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))  # Defina uma chave secreta segura
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Expiração do token (em segundos)

# initiating BD and the Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.seeds import seed_user

jwt = JWTManager(app)