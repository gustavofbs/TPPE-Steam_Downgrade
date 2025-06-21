# SteamRF - Plataforma de Jogos Digitais

SteamRF é uma plataforma de jogos digitais inspirada no Steam, com foco em funcionalidades de downgrade de jogos.

## Requisitos

- Docker
- Docker Compose

## Configuração e Execução

### Usando Docker (Recomendado)

1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd TPPE-Steam_Downgrade
   ```

2. Inicie os contêineres Docker:
   ```
   docker-compose up -d
   ```

3. Acesse a aplicação:
   - Web: http://localhost:8000
   - pgAdmin: http://localhost:5050
     - Email: admin@steamrf.com
     - Senha: admin

4. Para conectar ao PostgreSQL via pgAdmin:
   - Host: db
   - Porta: 5432
   - Usuário: postgres
   - Senha: postgres
   - Banco de dados: steamrf

5. Para criar um superusuário:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

6. Para parar os contêineres:
   ```
   docker-compose down
   ```

### Desenvolvimento Local (Sem Docker)

1. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure o banco de dados PostgreSQL localmente e atualize o arquivo `.env` conforme necessário.

4. Execute as migrações:
   ```
   python manage.py migrate
   ```

5. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

## Estrutura do Projeto

- `core/`: Aplicativo principal com funcionalidades da plataforma
- `users/`: Gerenciamento de usuários e perfis
- `steamrf/`: Configurações do projeto Django

## Funcionalidades Implementadas

- Sistema de autenticação completo (registro, login, recuperação de senha)
- Gerenciamento de perfil de usuário
- Interface básica para visualização de jogos (simulada)

## Próximos Passos

- Implementação completa do catálogo de jogos
- Sistema de compras
- Lista de desejos
- Sistema de amigos
- Avaliações e recomendações
- Administração avançada da plataforma
