# CI/CD Pipeline

Este diretório contém os workflows do GitHub Actions para o projeto Steam-Downgrade.

## 📋 Workflows Disponíveis

### 🔍 `lint.yml` - Verificação de Qualidade de Código
**Objetivo**: Workflow simples focado apenas em lint e qualidade de código.

**Triggers**:
- Push para branches: `main`, `develop`, `SteamRFv2`
- Pull requests para: `main`, `develop`

**Jobs**:
1. **Backend Lint** (`backend-lint`):
   - ✅ Black (formatação de código)
   - ✅ isort (ordenação de imports)
   - ✅ Flake8 (guia de estilo)

2. **Frontend Lint** (`frontend-lint`):
   - ✅ ESLint (linting JavaScript/TypeScript)
   - ✅ TypeScript type checking

3. **Lint Summary** (`lint-summary`):
   - ✅ Resumo dos resultados

### 🚀 `ci.yml` - Pipeline Completo
**Objetivo**: Pipeline completo com lint, testes, segurança e build.

**Jobs**:
1. **Backend Lint** - Qualidade de código Python
2. **Frontend Lint** - Qualidade de código TypeScript/React
3. **Backend Tests** - Testes automatizados com PostgreSQL
4. **Security Check** - Verificação de vulnerabilidades
5. **Docker Build** - Teste de build das imagens Docker

## 🛠️ Configurações de Lint

### Backend (Python)
- **Black**: Formatação de código (linha 88 caracteres)
- **isort**: Ordenação de imports
- **Flake8**: Verificação de estilo
- **Pylint**: Análise de qualidade de código

### Frontend (TypeScript/React)
- **ESLint**: Linting JavaScript/TypeScript
- **TypeScript**: Verificação de tipos
- **Next.js**: Build check

## 📁 Arquivos de Configuração

```
├── .flake8              # Configuração do Flake8
├── pyproject.toml       # Configuração Black, isort, Pylint
├── frontend/
│   ├── .eslintrc.json   # Configuração ESLint
│   └── tsconfig.json    # Configuração TypeScript
└── Makefile             # Comandos para desenvolvimento local
```

## 🚀 Executando Localmente

### Usando Makefile
```bash
# Instalar dependências
make install

# Executar todos os lints
make lint

# Executar apenas backend
make lint-backend

# Executar apenas frontend
make lint-frontend

# Formatar código automaticamente
make format
```

### Comandos Manuais

**Backend**:
```bash
# Instalar dependências de lint
pip install flake8 black isort

# Executar lints
black --check .
isort --check-only .
flake8 .

# Formatar código
black .
isort .
```

**Frontend**:
```bash
# Instalar dependências
cd frontend && npm install

# Executar lints
npm run lint
npm run type-check

# Formatar código
npm run lint -- --fix
```

## 🎯 Status Badges

Adicione ao README principal:

```markdown
![Lint Status](https://github.com/seu-usuario/TPPE-Steam_Downgrade/workflows/Lint%20Check/badge.svg)
![CI Status](https://github.com/seu-usuario/TPPE-Steam_Downgrade/workflows/CI%2FCD%20Pipeline/badge.svg)
```

## 🔧 Customização

Para modificar as regras de lint:

1. **Backend**: Edite `.flake8` e `pyproject.toml`
2. **Frontend**: Edite `frontend/.eslintrc.json`
3. **Workflows**: Edite os arquivos `.yml` neste diretório

## 📊 Métricas de Qualidade

O pipeline verifica:
- ✅ Formatação consistente de código
- ✅ Ordenação correta de imports
- ✅ Conformidade com guias de estilo
- ✅ Tipos TypeScript válidos
- ✅ Build sem erros
- ✅ Vulnerabilidades de segurança (pipeline completo)

## 🚨 Troubleshooting

### Erro de formatação Black
```bash
# Corrigir automaticamente
make format-backend
# ou
black .
```

### Erro de imports isort
```bash
# Corrigir automaticamente
isort .
```

### Erro ESLint
```bash
# Corrigir automaticamente
cd frontend && npm run lint -- --fix
```

### Erro TypeScript
```bash
# Verificar tipos
cd frontend && npm run type-check
```
