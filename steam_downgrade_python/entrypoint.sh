#!/bin/bash

# Espera pelo banco de dados
echo "Esperando pelo PostgreSQL..."
while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

# Cria as migrações e aplica
python manage.py makemigrations
python manage.py migrate

# Inicia o servidor
exec "$@"
