from config import db

class Account(db.Model):
    __tablename__ = 'conta'
    numero_conta = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float, nullable=False)

