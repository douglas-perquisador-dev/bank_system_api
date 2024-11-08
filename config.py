import os
import secrets
from flask import Flask
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

# Config JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))  # Defina uma chave secreta segura
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Expiração do token (em segundos)

# initiating BD and the Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.seeds import seed_user

jwt = JWTManager(app)