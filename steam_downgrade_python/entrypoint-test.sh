#!/bin/bash

# Espera pelo banco de dados
echo "Esperando pelo PostgreSQL..."
while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

# Cria o banco de dados de teste se não existir
echo "Verificando se o banco de dados de teste existe..."
PGPASSWORD=$SQL_PASSWORD psql -h $SQL_HOST -U $SQL_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$SQL_DATABASE'" | grep -q 1 || PGPASSWORD=$SQL_PASSWORD psql -h $SQL_HOST -U $SQL_USER -c "CREATE DATABASE $SQL_DATABASE;"
echo "Banco de dados de teste pronto"

# Executa os testes
exec "$@"
