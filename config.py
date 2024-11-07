import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initiating Flask
app = Flask(__name__)

# Config BD (RDS PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://postgres:D4q15g7b2@localhost:5432/bank_bd')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initiating BD and the Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import models for migrations
from models import accounts, transaction