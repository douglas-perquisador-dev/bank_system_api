# Bank System API

API para gerenciamento de sistema bancário desenvolvida com Flask, Flask-RESTX e SQLAlchemy.

## Índice

1. [Descrição do Projeto](#descrição-do-projeto)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração e Instalação](#configuração-e-instalação)
4. [Execução do Projeto](#execução-do-projeto)
5. [Testando a API](#testando-a-api)
6. [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

### Descrição do Projeto

Este projeto fornece uma API para criar, ler, atualizar e deletar informações de contas em um sistema bancário, com suporte a documentação Swagger para endpoints. A aplicação usa `Flask-RESTX` para a API, `SQLAlchemy` para a modelagem de dados e `PostgreSQL` como banco de dados.

### Pré-requisitos

Para rodar o projeto, é necessário ter:

- **Python 3.10 ou superior**
- **PostgreSQL 13** (ou superior)
- **Git** (opcional, para clonar o repositório)
- **Pipenv** ou **Virtualenv** (recomendado para ambientes virtuais)

### Configuração e Instalação

Siga as instruções abaixo para configurar o projeto:

#### Com Docker (recomendado)
1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/bank-system-api.git
   cd bank-system-api
   

2. Execute os containers:

    ```bash
    docker compose up --build -d
    ```
3. Acesse a documentação Swagger da API no navegador:

    - [http://localhost:5000/apidocs](http://localhost:5000/apidocs)
   
#### Sem Docker (execução local)

1. Clone o repositório:

    ```bash
    git clone https://github.com/seuusuario/bank_system_api.git
    cd bank_system_api
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Defina as variáveis de ambiente:
    - Renomeie o arquivo _.env.example_ para ._env_ e configure sua variaveis.

    ```bash
    DATABASE_URI=postgresql://objective:123456@postgres:5432/bank_system
   JWT_SECRET_KEY=b537a284d5e16e0996bac56cb01ff7abc13b5a9fab2f87ada5145fc6782b4247
   ```

5. Configure e inicie o banco de dados PostgreSQL (fora do escopo para execução local).

6. Execute as migrações do banco de dados:

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
## Execução do Projeto
Após configurar o ambiente e instalar as dependências, você pode executar o projeto.

1. Certifique-se de que o ambiente virtual esteja ativo.
2. Inicie o servidor Flask:
 ```bash
   python app.py
   ```
3. Acesse a aplicação no navegador em: http://localhost:5000
   - A documentação da API estará disponível em: http://localhost:5000/apidocs

4. Usuario de inicialização para uso;
   ```bash
   username='admin', password='123456'
   ```

## Testando a API

Execute os testes automatizados para validar a aplicação:

### Executar testes Automatizados 

```bash
pytest --maxfail=1 --tb=short -v
```
### Testar de forma manual
Para testar os endpoints da API, você pode usar ferramentas como Postman ou cURL, ou acessar diretamente a interface Swagger em http://localhost:5000/apidocs.


#### Endpoints principais
 - **GET /login:** Realiza a autenticação e retorna o token JWT.
    ```bash
   //Body json
    {
        "username": "admin",
        "password": "123456"
    }
    ```
   **OBS:** Com o Token retornado do login, adicione-o em _**Authorize**_ no seguinte formato: 
   ```bash
   Bearer <Token JWT>
   ```
- **POST /conta:** Cria uma nova Conta. Body:  
   ```bash
     //Body json
    { 
       "numero_conta": 234,
       "saldo": 180.37
    }
   ```
 - **GET /conta:** Retorna uma Conta pelo neu numero. _Param query: <numero_conta>_
 - **POST /transacao:** Cria uma transação em uma determinada conta.
   - **D:** Debito;
   - **C:** Crédito;
   - **P:** Pix;
    ```bash
   //Body json
    {
      "forma_pagamento": "D",
      "numero_conta": 237,
      "valor": 10
    }
    ```

### Tecnologias Utilizadas

 - Python 3
 - Flask
 - Flask-RESTX
 - SQLAlchemy
 - PostgreSQL
 - Docker (opcional para uso com containers)
