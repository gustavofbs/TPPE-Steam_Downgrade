# 🎮 Steam-Downgrade

**Plataforma de Jogos Digitais com Sistema de Downgrade**

> 📚 **Projeto Acadêmico** - Técnicas de Programação em Plataformas Emergentes (TPPE)  
> 🔄 **Refatoração** do [projeto original em Java](https://github.com/leomitx10/Steam-Downgrade) para Python/Django + Next.js

---

## 🚀 **Execução Rápida**

```bash
# Clonar e executar
git clone <url-do-repositorio>
cd TPPE-Steam_Downgrade
docker-compose up --build
```

**🌐 Acesso:**
- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8000
- **Admin:** http://localhost:8000/admin

---

## 📊 **Funcionalidades Implementadas**

### ✅ **Sistema Completo de Autenticação**
- Registro, login e perfis de usuário
- Upload de avatar e edição de dados
- Autenticação JWT segura

### ✅ **Catálogo de Jogos Avançado**
- Visualização com imagens, preços e promoções
- Sistema de busca com autocomplete em tempo real
- Páginas detalhadas com screenshots e informações

### ✅ **Sistema de Reviews Completo**
- Criar, editar e excluir avaliações
- Sistema de votos (útil/não útil)
- Cálculo automático de ratings e recomendações

### ✅ **Sistema de Compras**
- Carrinho de compras funcional
- Checkout com simulação de pagamento
- Histórico de pedidos

### ✅ **Painel Administrativo**
- Gerenciamento completo de jogos
- Upload de imagens e versões
- Interface Django Admin customizada

### 🚧 **Em Desenvolvimento**
- Sistema de amizades (busca e solicitações)
- Biblioteca pessoal de jogos
- Lista de desejos
- Filtros avançados no catálogo

---

## 📋 **Backlog Detalhado - Histórias de Usuário**

### 1. **Gerenciamento de Usuários**
- ✅ Criar conta na plataforma
- ✅ Fazer login na conta
- ✅ Editar perfil e upload de avatar
- ⏳ Recuperar senha por email

### 2. **Catálogo de Jogos**
- ✅ Visualizar jogos disponíveis na loja
- ✅ Visualizar detalhes de jogos específicos
- ✅ Filtrar jogos por categoria, preço, classificação
- ✅ Pesquisar jogos por nome (autocomplete implementado)

### 3. **Sistema de Compras**
- 🚧 Adicionar jogos ao carrinho
- 🚧 Remover jogos do carrinho
- 🚧 Finalizar compra (simulação)
- 🚧 Visualizar histórico de compras
- 🚧 Métodos de pagamento reais

### 4. **Avaliações e Reviews** ⭐
- ✅ Avaliar jogos possuídos
- ✅ Visualizar avaliações de outros usuários
- ✅ Votar em reviews (útil/não útil)
- ✅ Editar e excluir próprias avaliações
- 🚧 Sistema de recomendações baseado em preferências

### 5. **Sistema de Amigos**
- ✅ Adicionar outros usuários como amigos
- 🚧 Visualizar jogos dos amigos
- 🚧 Recomendar jogos para amigos
- ⏳ Chat entre amigos

### 6. **Biblioteca Pessoal**
- ✅ Visualizar jogos possuídos
- 🚧 Download de diferentes versões (downgrade)
- ⏳ Desinstalar jogos
- 🚧 Histórico de jogos recentes

### 7. **Lista de Desejos**
- 🚧 Adicionar jogos à lista de desejos
- 🚧 Remover jogos da lista
- ⏳ Notificações de promoções

### 8. **Administração**
- ✅ Adicionar novos jogos ao catálogo
- ✅ Editar informações de jogos
- ✅ Gerenciar versões de jogos
- ✅ Remover jogos do catálogo
- ✅ Gerenciar usuários

**Legenda:** ✅ Implementado | 🚧 Em Desenvolvimento | ⏳ Pendente

---

## **Stack Tecnológica**

**Backend:** Django 4.2 + DRF + PostgreSQL + JWT  
**Frontend:** Next.js 14 + TypeScript + Tailwind CSS  
**DevOps:** Docker + Docker Compose  

---

## **Arquitetura**

```
┌─────────────────┐    HTTP/JSON   ┌─────────────────┐
│   FRONTEND      │◄──────────────►│    BACKEND      │
│   (Next.js)     │                │   (Django)      │
│                 │                │                 │
│ • Componentes   │                │ • API REST      │
│ • Contexts      │                │ • Models        │
│ • Services      │                │ • ViewSets      │
└─────────────────┘                └─────────────────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │   PostgreSQL    │
                                   │   (Database)    │
                                   └─────────────────┘
```

**Padrões Utilizados:**
- **Backend:** MV + Modular Apps + API-First
- **Frontend:** Component-Based + Context Pattern
- **Comunicação:** RESTful APIs

---

## 📋 **Pré-requisitos**

- Docker
- Docker Compose

---

## 📚 **Documentação Adicional**

- **🐳 Docker:** [`DOCKER.md`](./DOCKER.md)
- **📊 UML:** [Diagramas de Classe](https://app.mural.co/t/unb0369/m/unb0369/1746670269569/d64fd62544c0730b4e62710beeeeaea87658c3f9)
- **💾 Original:** [Steam-Downgrade Java](https://github.com/leomitx10/Steam-Downgrade)
