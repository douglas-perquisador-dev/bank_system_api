from typing import Optional
from config import db
from models.accounts import Account

class AccountRepository:
    @staticmethod
    def create_account(num_account: int, balance: float) -> Account:
        """
        Cria uma nova conta com um numero e um saldo

        :param num_account:
        :param balance:
        :return: Account
        """
        account = Account(numero_conta=num_account, saldo=balance)
        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def get_account(num_account: int) -> Optional[Account]:
        """
        Retorna os dados de uma conta de acordo com o numero requerido

        :param num_account:
        :return:  Account
        """
        return Account.query.filter_by(numero_conta=num_account).first()

    @staticmethod
    def update_balance(account: Account) -> Optional[Account]:
        """
         Atualiza Saldo em conta de  acordo com o numero requerido

        :param account: Conta com saldo atualizado
        :return: Account
        """
        if account:
            db.session.commit()
        return account

