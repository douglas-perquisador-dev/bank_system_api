from repositories.account import AccountRepository
from repositories.transaction import TransactionRepository
from models.accounts import Account
from enums.transaction_enum import PaymentMethod

class AccountService:
    @staticmethod
    def create_account(account_number: int, balance: float) -> Account:
        if AccountRepository.get_account(account_number):
            raise ValueError("Conta Já existente")
        return AccountRepository.create_account(account_number, balance)

    @staticmethod
    def get_account(account_number: int) -> Account:
        account = AccountRepository.get_account(account_number)
        if not account:
            raise ValueError("Conta não encontrada")
        return account

    @staticmethod
    def process_transaction(account_number: int, payment_method: PaymentMethod, amount: float) -> Account:
        account = AccountRepository.get_account(account_number)
        if not account:
            raise ValueError("Conta não encontrada")

        fee: float = 0.0
        if payment_method == PaymentMethod.DEBIT_CARD:
            fee = 0.03
        elif payment_method == PaymentMethod.CREDIT_CARD:
            fee = 0.05

        amount_with_fee: float = amount * (1 + fee)

        if account.saldo < amount_with_fee:
            raise ValueError("Saldo insuficiente")

        AccountRepository.update_balance(account_number, account.saldo - amount_with_fee)
        TransactionRepository.register_transaction(account_number, payment_method, amount)
        return account
