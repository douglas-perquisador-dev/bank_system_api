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

## Organização e Estrutura do projeto (Design Pattern)
**Design Pattern: Layered Architecture**
- Separação de Preocupações: Camadas claramente definidas impedem que a lógica vaze entre componentes.
Reutilização do Código: A lógica de negócios é encapsulada em serviços, facilitando a reutilização.
- Testabilidade: Cada camada pode ser testada em unidade isoladamente, melhorando a confiabilidade do código.
- Escalabilidade: Novos recursos podem ser adicionados mais facilmente, pois a responsabilidade de cada camada é bem definida.
Este padrão de design tornará seu aplicativo mais sustentável e mais fácil de escalar à medida que ele cresce.

A arquitetura é organizada em camadas, o que facilita a manutenção, escalabilidade e entendimento do código. As camadas principais são:

**Controllers (Camada de Apresentação/Interface)**
Arquivos: auth.py, transaction.py
Função: Gerencia as rotas e a lógica relacionada a requisições e respostas HTTP.
Ex.: AuthController e TransactionController são responsáveis por lidar com as requisições de autenticação e transações.

**Services (Camada de Negócio/Aplicação)**
Arquivo: account.py
Função: Implementa a lógica de negócios, processando os dados recebidos da camada de apresentação.
Ex.: AccountService gerencia a criação e manipulação de contas bancárias.

**Repositories (Camada de Acesso a Dados)**
Arquivos: account.py, transaction.py
Função: Comunicação com o banco de dados, utilizando os modelos definidos.
Ex.: AccountRepository acessa diretamente os dados de contas no banco.

**Models (Camada de Modelagem de Dados)**
Arquivos: accounts.py, transactions.py, users.py
Função: Definem as estruturas e relacionamentos das tabelas no banco de dados.
Ex.: O modelo Account representa a tabela de contas.

**Enums (Enumeração de Constantes)**
Arquivo: transaction_enum.py
Função: Define constantes usadas em transações, como os métodos de pagamento.

**Configuração e Infraestrutura**
Dockerfile, docker-compose.yml, .env, config.py, entrypoint.sh
Função: Configurações de ambiente, banco de dados e inicialização da aplicação.

**Testes**
test_app.py
Função: Testes unitários e de integração.

## Swegger
A documentação do projeto é feita utilizando o pacote Flasgger, que permite documentar e testar os endpoints da sua aplicação Flask de forma simples e intuitiva.
```
#Exemplo uso do swegger em cada class/funcionalidade do sistema
 @swag_from({
        'tags': ['Account'],
        'security': [{'Bearer': []}],
        'parameters': []
        })

**Termos e configurações utilizadas**
- info: Informações gerais da API. 
- tags: Define a seção da documentação (neste caso, "Autenticação").
- security: Indica que o endpoint exige um token JWT (Bearer).
- securityDefinitions: Define o esquema de autenticação (Bearer).
- enum: Define valores fixos para o campo forma_pagamento.
- description: Explica o propósito do endpoint.
- parameters: Lista os parâmetros esperados (neste caso, username e password).
- example: Exemplo de payload esperado.
- responses: Descreve as possíveis respostas (201, 200 e 404).

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
