FROM python:3.9-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir diretório de trabalho
WORKDIR /code

# Instalar dependências do sistema e Python
RUN apt-get update && apt-get install -y netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar o entrypoint script
COPY ./steam_downgrade_python/entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh && \
    sed -i 's/\r$//' /code/entrypoint.sh

# Copiar o projeto
COPY ./steam_downgrade_python /code/

# Definir o entrypoint
ENTRYPOINT ["/code/entrypoint.sh"]
