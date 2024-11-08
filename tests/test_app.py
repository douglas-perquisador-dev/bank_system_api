import random

import pytest
from unittest.mock import patch
from flask.testing import FlaskClient
from app import app, db
from models.accounts import Account
from repositories.account import AccountRepository
from repositories.transaction import TransactionRepository
from services.account import AccountService
from models.users import User
from werkzeug.security import generate_password_hash

# Definindo o número aleatorio da conta que será usado para o teste
numero_conta = random.randint(1000, 9999)

@pytest.fixture
def client() -> FlaskClient:
    """Inicializa o cliente de testes com contexto da aplicação"""
    with app.app_context():  # Aqui está a correção: garantir o contexto da app
        with app.test_client() as client:
            # Cria o banco de dados e popula com dados iniciais
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def admin_user(client: FlaskClient) -> User:
    """Cria o usuário admin no banco de dados para ser usado nos testes"""
    user = User(username='test', password='123456')
    user.set_password('123456')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def jwt_token(client: FlaskClient, admin_user: User) -> str:
    """Obtém o token JWT após o login do usuário admin"""
    response = client.post('/login', json={'username': 'test', 'password': '123456'})
    assert response.status_code == 200
    return response.get_json()['access_token']

## TESTES DE AUTENTICAÇÃO
def test_login_success(client: FlaskClient, admin_user: User) -> None:
    """Testa o login do usuário admin e obtenção do JWT."""
    response = client.post('/login', json={"username": "test", "password": "123456"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_invalido(client: FlaskClient) -> None:
    """Testa o login com credenciais inválidas."""
    response = client.post('/login', json={"username": "test", "password": "senhaerrada"})
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"

def test_protect_route_sem_jwt(client: FlaskClient) -> None:
    """Testa a proteção de rotas que exigem autenticação JWT sem fornecer o token."""
    response = client.get('/conta')
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Missing Authorization Header"

def test_protect_route_com_jwt(client: FlaskClient, admin_user: User, jwt_token: str) -> None:
    """Testa a proteção de rotas com autenticação JWT."""
    response = client.get(
        '/conta',
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 200


## TESTES DE FUNCIONALIDADES E REGRA DE NEGOCIO
def test_criar_conta(client: FlaskClient, jwt_token: str) -> None:
    """Testa a criação de uma conta bancária."""
    response = client.post(
        '/conta',
        json={"numero_conta": numero_conta, "saldo": 200.0},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 201
    assert response.get_json()["numero_conta"] == numero_conta


def test_criar_conta_existente(client: FlaskClient, jwt_token: str) -> None:
    """Testa a criação de uma conta bancária com número já existente."""

    # Criando a conta no banco pela primeira vez
    response_create = client.post(
        '/conta',
        json={"numero_conta": numero_conta, "saldo": 200.0},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    # Verifica que a primeira criação foi bem-sucedida (201)
    assert response_create.status_code == 201

    # Agora, tentando criar a mesma conta novamente
    response_create_again = client.post(
        '/conta',
        json={"numero_conta": numero_conta, "saldo": 200.0},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    # Verifica que a segunda tentativa de criação da conta retorna um erro 404
    assert response_create_again.status_code == 404

    # Verifica que a mensagem de erro está correta
    assert response_create_again.get_json()["error"] == "Conta Já existente"


def test_consultar_conta_inexistente(client: FlaskClient, jwt_token: str) -> None:
    """Testa a criação de uma conta bancária."""
    response = client.get(
        '/conta',
        query_string={"numero_conta": 99999},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Conta não encontrada"

def test_transacao_saldo_insuficiente(client: FlaskClient, mocker, jwt_token: str) -> None:
    """Testa a transação quando o saldo é insuficiente."""
    mocker.patch.object(AccountService, 'process_transaction', side_effect=ValueError("Saldo insuficiente"))

    response = client.post(
        '/transacao',
        json={"numero_conta": numero_conta, "forma_pagamento": "D", "valor": 1},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Saldo insuficiente"

def test_transacao_debito_sucesso(client: FlaskClient, mocker, jwt_token: str) -> None:
    """Testa a transação quando há saldo suficiente."""

    # Mock para `get_account` retornando uma conta com saldo suficiente
    mocker.patch.object(AccountRepository, 'get_account', return_value=Account(numero_conta=numero_conta, saldo=200.0))

    # Mock para `update_balance` para evitar atualização real no banco
    mocker.patch.object(AccountRepository, 'update_balance', return_value=None)

    # Mock para `register_transaction` para evitar transação real no banco
    mocker.patch.object(TransactionRepository, 'register_transaction', return_value=None)

    response = client.post(
        '/transacao',
        json={"numero_conta": numero_conta, "forma_pagamento": "D", "valor": 100.0},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    # Verifica se a transação foi bem-sucedida
    assert response.status_code == 201  # Espera o status 201 para criação
    assert response.get_json()["numero_conta"] == numero_conta
    assert response.get_json()["saldo"] == 97

def test_transacao_credito_sucesso(client: FlaskClient, mocker, jwt_token: str) -> None:
    """Testa a transação quando há saldo suficiente."""

    # Mock para `get_account` retornando uma conta com saldo suficiente
    mocker.patch.object(AccountRepository, 'get_account', return_value=Account(numero_conta=numero_conta, saldo=200.0))

    # Mock para `update_balance` para evitar atualização real no banco
    mocker.patch.object(AccountRepository, 'update_balance', return_value=None)

    # Mock para `register_transaction` para evitar transação real no banco
    mocker.patch.object(TransactionRepository, 'register_transaction', return_value=None)

    response = client.post(
        '/transacao',
        json={"numero_conta": numero_conta, "forma_pagamento": "C", "valor": 100.0},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    # Verifica se a transação foi bem-sucedida
    assert response.status_code == 201  # Espera o status 201 para criação
    assert response.get_json()["numero_conta"] == numero_conta
    assert response.get_json()["saldo"] == 95

def test_transacao_pix_sucesso(client: FlaskClient, mocker, jwt_token: str) -> None:
    """Testa a transação quando há saldo suficiente."""

    # Mock para `get_account` retornando uma conta com saldo suficiente
    mocker.patch.object(AccountRepository, 'get_account', return_value=Account(numero_conta=numero_conta, saldo=200.0))

    # Mock para `update_balance` para evitar atualização real no banco
    mocker.patch.object(AccountRepository, 'update_balance', return_value=None)

    # Mock para `register_transaction` para evitar transação real no banco
    mocker.patch.object(TransactionRepository, 'register_transaction', return_value=None)

    response = client.post(
        '/transacao',
        json={"numero_conta": numero_conta, "forma_pagamento": "P", "valor": 100.0},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    # Verifica se a transação foi bem-sucedida
    assert response.status_code == 201  # Espera o status 201 para criação
    assert response.get_json()["numero_conta"] == numero_conta
    assert response.get_json()["saldo"] == 100


