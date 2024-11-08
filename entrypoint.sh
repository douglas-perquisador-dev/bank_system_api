#!/bin/bash

# Rodar as migrações do banco
flask db init
flask db migrate -m "Initial migration"
flask db upgrade


pytest --maxfail=1 --tb=short -v

if [ $? -eq 0 ]; then
    echo "Todos os testes passaram! Iniciando o servidor..."
    # Rodar os seeds
    flask seed_user
    # Iniciar o servidor Flask
    flask run --host=0.0.0.0 --port=5000
else
    echo "Testes falharam. Servidor não será iniciado."
    exit 1
fi
