## Visão Geral

  Projeto de refatoração do Steam Downgrade, um trabalho de Orientação de Objetos.


## Backlog de Histórias de Usuário - Steam Downgrade

### Épicos

### 1. Gerenciamento de Usuários
- **Como** usuário não registrado, **quero** poder criar uma conta na plataforma **para** acessar os recursos da loja de jogos.
- **Como** usuário registrado, **quero** poder fazer login na minha conta **para** acessar meus jogos e informações pessoais.
- **Como** usuário registrado, **quero** poder editar meu perfil **para** manter minhas informações atualizadas.
- **Como** usuário registrado, **quero** poder recuperar minha senha **para** recuperar acesso à minha conta caso a esqueça.

### 2. Catálogo de Jogos
- **Como** usuário, **quero** poder visualizar os jogos disponíveis na loja **para** descobrir novos títulos.
- **Como** usuário, **quero** poder filtrar jogos por categoria, preço ou classificação **para** encontrar jogos de meu interesse mais facilmente.
- **Como** usuário, **quero** poder visualizar detalhes de um jogo específico **para** decidir se desejo comprá-lo.
- **Como** usuário, **quero** poder pesquisar jogos por nome **para** encontrar rapidamente um título específico.

### 3. Gerenciamento de Biblioteca
- **Como** usuário, **quero** poder visualizar os jogos que possuo **para** acessá-los facilmente.
- **Como** usuário, **quero** poder baixar e instalar jogos da minha biblioteca **para** jogar em meu computador.
- **Como** usuário, **quero** poder desinstalar jogos **para** liberar espaço em meu computador.
- **Como** usuário, **quero** poder ver o histórico de jogos que joguei recentemente **para** retomar de onde parei.

### 4. Sistema de Compras
- **Como** usuário, **quero** poder adicionar jogos ao carrinho de compras **para** adquiri-los posteriormente.
- **Como** usuário, **quero** poder remover jogos do carrinho **para** ajustar minha compra.
- **Como** usuário, **quero** poder finalizar a compra dos jogos no carrinho **para** adicioná-los à minha biblioteca.
- **Como** usuário, **quero** poder escolher diferentes métodos de pagamento **para** concluir minhas compras de forma conveniente.
- **Como** usuário, **quero** poder visualizar o histórico de compras **para** controlar meus gastos na plataforma.

### 5. Lista de Desejos
- **Como** usuário, **quero** poder adicionar jogos à minha lista de desejos **para** acompanhá-los e comprá-los futuramente.
- **Como** usuário, **quero** poder remover jogos da minha lista de desejos **para** mantê-la atualizada.
- **Como** usuário, **quero** ser notificado quando jogos da minha lista de desejos estiverem em promoção **para** aproveitar descontos.

### 6. Sistema de Amigos
- **Como** usuário, **quero** poder adicionar outros usuários como amigos **para** interagir com eles na plataforma.
- **Como** usuário, **quero** poder visualizar os jogos que meus amigos possuem **para** descobrir novos títulos.
- **Como** usuário, **quero** poder enviar mensagens para meus amigos **para** comunicar-me com eles.

### 7. Avaliações e Recomendações
- **Como** usuário, **quero** poder avaliar jogos que possuo **para** compartilhar minha opinião com outros usuários.
- **Como** usuário, **quero** poder visualizar avaliações de outros usuários **para** tomar decisões de compra mais informadas.
- **Como** usuário, **quero** receber recomendações de jogos baseadas em minhas preferências **para** descobrir novos títulos que possam me interessar.

### 8. Administração da Plataforma
- **Como** administrador, **quero** poder adicionar novos jogos ao catálogo **para** manter a loja atualizada.
- **Como** administrador, **quero** poder editar informações de jogos existentes **para** corrigir dados ou atualizar detalhes.
- **Como** administrador, **quero** poder remover jogos do catálogo **para** manter a qualidade da loja.
- **Como** administrador, **quero** poder gerenciar usuários **para** garantir o bom funcionamento da plataforma.

## Priorização

### Alta Prioridade
1. Criação e login de conta de usuário
2. Visualização do catálogo de jogos
3. Visualização de detalhes de jogos
4. Adição de jogos ao carrinho
5. Finalização de compra
6. Visualização da biblioteca de jogos

### Média Prioridade
1. Edição de perfil de usuário
2. Filtros e pesquisa no catálogo
3. Lista de desejos
4. Histórico de compras
5. Avaliações de jogos

### Baixa Prioridade
1. Sistema de amigos
2. Sistema de recomendações
3. Recuperação de senha
4. Histórico de jogos recentes
5. Notificações de promoções

### UML 
https://app.mural.co/t/unb0369/m/unb0369/1746670269569/d64fd62544c0730b4e62710beeeeaea87658c3f9

# Instruções para Steam Downgrade

Aqui contém instruções para executar o ambiente Docker do projeto Steam Downgrade.

## Pré-requisitos

- Docker
- Docker Compose

## Estrutura do Projeto

O ambiente Docker consiste em quatro serviços principais:

1. **web**: Aplicação Django
2. **db**: Banco de dados PostgreSQL
3. **pgadmin**: Interface web para gerenciamento do PostgreSQL
4. **tests**: Serviço para execução de testes TDD (configurado para ignorar os testes)

## Como Executar

1. Certifique-se de que o Docker e o Docker Compose estão instalados e em execução
2. Navegue até o diretório raiz do projeto (onde está o arquivo `docker-compose.yml`)
3. Execute o comando:

```bash
docker-compose up --build
```

4. Aguarde até que todos os serviços sejam iniciados. O script de inicialização irá:
   - Esperar pelo PostgreSQL estar disponível
   - Criar e aplicar as migrações do Django
   - Iniciar o servidor Django

## Acessando os Serviços

- **Aplicação Django**: http://localhost:8000
- **API REST**: http://localhost:8000/api/hello/
- **pgAdmin**: http://localhost:5050
  - Email: admin@admin.com
  - Senha: admin

## Configurando o pgAdmin

1. Acesse http://localhost:5050 e faça login com as credenciais acima
2. Clique em "Add New Server"
3. Na aba "General", dê um nome ao servidor (ex: "Steam Downgrade DB")
4. Na aba "Connection", preencha:
   - Host name/address: `db` (nome do serviço no docker-compose)
   - Port: `5432`
   - Maintenance database: `steam_downgrade`
   - Username: `postgres`
   - Password: `postgres`
5. Clique em "Save"

## Testes

Os testes estão configurados para serem ignorados, conforme solicitado. Para verificar isso, execute:

```bash
docker-compose run tests
```

Você verá uma mensagem indicando que os testes foram ignorados.

## Solução de Problemas

### Erro de permissão no entrypoint.sh

Se você encontrar um erro como:
```
OCI runtime create failed: unable to start container process: exec: "/code/entrypoint.sh": permission denied
```

Certifique-se de que o arquivo `entrypoint.sh` tem permissões de execução:

```bash
chmod +x steam_downgrade_python/entrypoint.sh
```

### Problemas com caracteres de fim de linha (CRLF vs LF)

Se você estiver desenvolvendo em Windows e implantando em Linux, pode haver problemas com os caracteres de fim de linha. O Dockerfile já inclui um comando para converter CRLF para LF, mas se ainda houver problemas, você pode converter manualmente:

```bash
# No Linux
sed -i 's/\r$//' steam_downgrade_python/entrypoint.sh
```

ou usar uma ferramenta como o dos2unix:

```bash
dos2unix steam_downgrade_python/entrypoint.sh
```

    

