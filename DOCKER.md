# 🐳 Docker Setup - Steam-Downgrade

Este guia explica como executar o Steam-Downgrade usando Docker com frontend e backend totalmente containerizados.

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🚀 Execução Rápida

### Desenvolvimento
```bash
# Construir e executar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d --build
```

### Produção
```bash
# Usar configuração de produção
docker-compose -f docker-compose.prod.yml up --build

# Executar em background
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🌐 Acesso aos Serviços

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost:3001 | Interface Next.js |
| **Backend API** | http://localhost:8000 | Django REST API |
| **PgAdmin** | http://localhost:5050 | Administração PostgreSQL |
| **Database** | localhost:5432 | PostgreSQL |

### Credenciais PgAdmin
- **Email:** admin@steamrf.com
- **Senha:** admin

## 📁 Estrutura dos Containers

```
┌─────────────────────────────────────────┐
│                Frontend                 │
│            (Next.js)                    │
│         localhost:3001                  │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│                Backend                  │
│            (Django)                     │
│         localhost:8000                  │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│              Database                   │
│           (PostgreSQL)                  │
│         localhost:5432                  │
└─────────────────────────────────────────┘
```

## 🛠️ Comandos Úteis

### Gerenciamento dos Containers
```bash
# Ver logs de todos os serviços
docker-compose logs

# Ver logs de um serviço específico
docker-compose logs frontend
docker-compose logs web
docker-compose logs db

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: remove dados do banco)
docker-compose down -v

# Rebuild apenas um serviço
docker-compose up --build frontend
docker-compose up --build web
```

### Executar Comandos nos Containers
```bash
# Acessar shell do backend
docker-compose exec web sh

# Executar migrações manualmente
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Acessar shell do frontend
docker-compose exec frontend sh

# Instalar nova dependência no frontend
docker-compose exec frontend npm install <package>
```

### Desenvolvimento
```bash
# Rebuild após mudanças no Dockerfile
docker-compose up --build

# Ver status dos containers
docker-compose ps

# Limpar containers, redes e imagens não utilizadas
docker system prune
```

## 🔧 Configurações

### Variáveis de Ambiente

#### Backend (Django)
- `DB_HOST=db`
- `DB_NAME=steamrf`
- `DB_USER=postgres`
- `DB_PASS=postgres`
- `DEBUG=1` (desenvolvimento) / `DEBUG=0` (produção)

#### Frontend (Next.js)
- `NODE_ENV=development` (desenvolvimento) / `NODE_ENV=production` (produção)
- `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`

### Volumes

#### Desenvolvimento
- **Frontend:** `./frontend:/app` - Hot reload habilitado
- **Backend:** `.:/app` - Hot reload habilitado
- **Database:** `postgres_data:/var/lib/postgresql/data/` - Dados persistentes

#### Produção
- **Database:** `postgres_data:/var/lib/postgresql/data/` - Dados persistentes
- Sem volumes de código (imagens otimizadas)

## 📦 Dockerfiles

### Frontend
- **`Dockerfile`** - Produção (multi-stage, otimizado)
- **`Dockerfile.dev`** - Desenvolvimento (hot reload)

### Backend
- **`Dockerfile`** - Django com Python 3.11

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Erro de conexão com banco
```bash
# Verificar se o banco está rodando
docker-compose ps db

# Ver logs do banco
docker-compose logs db

# Reiniciar apenas o banco
docker-compose restart db
```

#### 2. Frontend não conecta com backend
```bash
# Verificar se o backend está rodando
curl http://localhost:8000/api/v1/

# Verificar logs do backend
docker-compose logs web

# Verificar variável de ambiente
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL
```

#### 3. Mudanças no código não aparecem
```bash
# Para desenvolvimento, verificar se volumes estão corretos
docker-compose down
docker-compose up --build

# Para produção, sempre rebuild
docker-compose -f docker-compose.prod.yml up --build
```

#### 4. Erro de permissões
```bash
# Linux/Mac: ajustar permissões
sudo chown -R $USER:$USER ./frontend/node_modules
sudo chown -R $USER:$USER ./.next
```

### Limpeza Completa
```bash
# Parar tudo e limpar
docker-compose down -v
docker system prune -a
docker volume prune

# Rebuild completo
docker-compose up --build
```

## 🚀 Deploy

### Desenvolvimento Local
```bash
docker-compose up --build
```

### Produção
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### CI/CD
```bash
# Build para produção
docker-compose -f docker-compose.prod.yml build

# Push para registry (se necessário)
docker tag steamdowngrade_frontend:latest your-registry/steamdowngrade_frontend:latest
docker push your-registry/steamdowngrade_frontend:latest
```

## 📚 Próximos Passos

1. **Nginx Reverse Proxy** - Para produção
2. **SSL/HTTPS** - Certificados
3. **Monitoring** - Logs centralizados
4. **Backup** - Estratégia de backup do banco
5. **Scaling** - Docker Swarm ou Kubernetes

---

**🎮 Steam-Downgrade agora está totalmente dockerizado! 🐳**
