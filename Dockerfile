FROM python:3.12-slim as base

# Instalar as dependências necessárias para compilar o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

#COPY requirements.txt /app/requirements.txt
COPY . /app/

RUN pip install --no-cache-dir -r requirements_linux.txt

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

