from datetime import datetime
from config import db
from enums import transaction_enum
from models.transactions import Transaction


class TransacaoRepository:
    @staticmethod
    def registrar_transacao(num_account: int, payment: transaction_enum.FormaPagamento, value: float) -> Transaction:
        transaction = Transaction(
            numero_conta=num_account,
            forma_pagamento=payment,
            valor=value,
            data_transacao=datetime.now()
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction