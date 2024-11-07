import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initiating Flask
app = Flask(__name__)

# Config BD (RDS PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://objective:123456@localhost/bank_bd')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initiating BD
db = SQLAlchemy(app)
