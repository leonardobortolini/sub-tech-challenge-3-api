# TRABALHO SUBSTITUTIVO DE TECH CHALLENGE - FASE 3 API

API responsável pelo cadastro, gerenciamento e venda de veículos.

A solução foi desenvolvida utilizando uma arquitetura baseada em DDD, com separação entre domínio, aplicação, infraestrutura e apresentação.

A autenticação e autorização dos usuários são realizadas por um serviço independente baseado em Keycloak, mantido em um repositório separado.

## Funcionalidades

- Cadastro de veículos para venda
- Edição dos dados dos veículos
- Listagem de veículos disponíveis
- Listagem de veículos vendidos
- Compra de veículos por usuários autenticados
- Validação de CPF do comprador
- Controle de status dos veículos
- Controle de status dos pagamentos
- Atualização de pagamentos através de webhook
- Autenticação utilizando JWT
- Autorização baseada em roles

As listagens de veículos disponíveis e vendidos são ordenadas pelo preço, do menor para o maior.

---

## Tecnologias

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker
- Docker Compose
- Kubernetes
- Minikube
- Keycloak
- Pytest
- GitHub Actions

---

## Arquitetura

A solução é composta por dois projetos independentes:

```text
┌─────────────────────────────────┐
│          Projeto Auth           │
│                                 │
│       Keycloak + PostgreSQL     │
│                                 │
│  Autenticação e gerenciamento   │
│          de usuários            │
└────────────────┬────────────────┘
                 │
                 │ JWT
                 ▼
┌─────────────────────────────────┐
│           Projeto API           │
│                                 │
│       FastAPI + PostgreSQL      │
│                                 │
│  Veículos / Vendas / Pagamentos │
└─────────────────────────────────┘
```

O serviço de autenticação possui seu próprio banco de dados e não compartilha o utilizado pela API.

## Repositórios

- [sub-tech-challenge-3-auth](https://github.com/leonardobortolini/sub-tech-challenge-3-auth) — serviço de autenticação baseado em Keycloak.
- [sub-tech-challenge-3-api](https://github.com/leonardobortolini/sub-tech-challenge-3-api) — API responsável pelas operações de veículos, vendas e pagamentos.

Para executar a solução completa localmente, os dois projetos devem estar disponíveis.

---

## Estrutura do projeto

```text
src/

├── dominio
│   ├── entidades
│   ├── enums
│   ├── excecoes
│   ├── repositorios
│   └── validacao
│
├── aplicacao
│   ├── casos_de_uso
│   └── schemas
│
├── infraestrutura
│   ├── autenticacao
│   └── database
│
└── apresentacao
    └── controllers
```

---

# Separação da autenticação

A autenticação e o gerenciamento dos usuários são realizados por um serviço independente baseado em Keycloak.

O serviço de autenticação possui seu próprio PostgreSQL e é executado separadamente da API.

A API não armazena os dados cadastrais dos usuários. Após a autenticação, o Keycloak emite um JWT contendo as informações necessárias para autenticação e autorização.

Durante a venda, a API utiliza o `sub` presente no JWT para identificar o usuário responsável pela operação.

Dessa forma:

```text
Keycloak
   │
   ├── Usuários
   ├── Roles
   └── Autenticação
          │
          │ JWT
          ▼
       API
          │
          ├── Veículos
          ├── Vendas
          └── Pagamentos
```

Os dados relacionados à autenticação permanecem no serviço Auth, enquanto os dados transacionais permanecem no banco da API.

---

# Autenticação e autorização

A API utiliza JWT emitido pelo Keycloak.

As principais roles utilizadas são:

- `admin`
- `cliente`

Os endpoints protegidos devem receber o token através do header:

```text
Authorization: Bearer <TOKEN>
```

## Matriz de autorização

| Método | Endpoint | Autenticação | Role |
|---|---|---|---|
| POST | `/veiculos` | JWT | `admin` |
| PUT | `/veiculos/{id}` | JWT | `admin` |
| GET | `/veiculos/disponiveis` | JWT | Usuário autenticado |
| GET | `/veiculos/vendidos` | JWT | `admin` |
| POST | `/veiculos/{id}/vender` | JWT | `cliente` |
| POST | `/pagamentos/webhook` | Não | — |
| GET | `/pagamentos` | Não | — |

---

# Pré-requisitos

### Execução com Docker

- Docker
- Docker Compose

### Execução com Kubernetes

- Docker
- kubectl
- Minikube

### Desenvolvimento e testes

- Python 3.12

---

# Executando a solução localmente

A execução completa da solução depende dos dois projetos:

- `sub-tech-challenge-3-auth`
- `sub-tech-challenge-3-api`

Recomenda-se manter os projetos em diretórios próximos:

```text
projetos/
├── sub-tech-challenge-3-auth/
└── sub-tech-challenge-3-api/
```

> O serviço Auth deve ser iniciado **antes da API**.
> O Keycloak é responsável pela autenticação e autorização dos usuários e precisa estar disponível para que a API consiga validar os tokens JWT.

A ordem recomendada para executar a solução é:

```text
1. Iniciar o Auth
       ↓
2. Verificar o Keycloak
       ↓
3. Criar usuários e roles
       ↓
4. Obter um JWT
       ↓
5. Iniciar a API
       ↓
6. Utilizar o JWT nos endpoints protegidos
```

---

## 1. Iniciar o serviço de autenticação

Primeiro, entre no diretório do projeto Auth:

```bash
cd sub-tech-challenge-3-auth
```

Inicie o ambiente:

```bash
docker compose up -d
```

O projeto Auth irá iniciar:

- Keycloak
- PostgreSQL utilizado pelo Keycloak
- Rede Docker utilizada pela solução

Verifique os containers:

```bash
docker compose ps
```

O Keycloak ficará disponível em:

```text
http://localhost:8080
```

O realm utilizado pela aplicação é:

```text
revenda
```

> O projeto Auth deve permanecer em execução enquanto a API estiver sendo utilizada localmente.

---

## 2. Verificar o Keycloak

Após iniciar o Auth, valide se o realm está disponível:

```bash
curl -s   http://localhost:8080/realms/revenda/.well-known/openid-configuration
```

A resposta deve conter as informações do OpenID Connect, incluindo o `issuer` e o endpoint de emissão de tokens.

Exemplo:

```json
{
  "issuer": "http://localhost:8080/realms/revenda",
  "token_endpoint": "http://localhost:8080/realms/revenda/protocol/openid-connect/token"
}
```

---

## 3. Criar usuários e roles

O Keycloak utiliza as seguintes roles:

- `admin`
- `cliente`

Os usuários utilizados pela aplicação devem ser criados **manualmente através da interface administrativa do Keycloak**.

Acesse:

```text
http://localhost:8080
```

Selecione o realm:

```text
revenda
```

Crie os usuários que serão utilizados durante os testes e atribua as roles necessárias.

### Roles disponíveis

| Role | Permissões |
|---|---|
| `admin` | Cadastrar e editar veículos e consultar veículos vendidos |
| `cliente` | Realizar a compra de veículos |
| Usuário autenticado | Consultar veículos disponíveis |

> A criação dos usuários e a atribuição das roles não são realizadas automaticamente pela API.

---

## 4. Obter um token de autenticação

Para utilizar os endpoints protegidos da API, é necessário obter um JWT através do Keycloak.

O endpoint utilizado é:

```text
POST /realms/revenda/protocol/openid-connect/token
```

Utilize as credenciais de um dos usuários criados anteriormente.

Exemplo no Docker:

```bash
curl -X POST   http://localhost:8080/realms/revenda/protocol/openid-connect/token   -H "Content-Type: application/x-www-form-urlencoded"   -d "client_id=revenda-api"   -d "username=USUARIO"   -d "password=SENHA"   -d "grant_type=password"
```

Exemplo no Kubernetes:

```bash
curl -X POST   http://localhost:18081/realms/revenda/protocol/openid-connect/token   -H "Content-Type: application/x-www-form-urlencoded"   -d "client_id=revenda-api"   -d "username=USUARIO"   -d "password=SENHA"   -d "grant_type=password"
```

A resposta conterá um `access_token`:

```json
{
  "access_token": "eyJ...",
  "expires_in": 1800,
  "token_type": "Bearer"
}
```

Copie o valor do `access_token`, pois ele será utilizado para acessar os endpoints protegidos da API.

---

# 5. Iniciar a API com Docker Compose

> **Pré-requisito:** o projeto Auth deve estar em execução antes de iniciar a API.

Entre no diretório da API:

```bash
cd ../sub-tech-challenge-3-api
```

Execute:

```bash
docker compose up --build
```

Após a inicialização, a API ficará disponível em:

```text
http://localhost:8000
```

A documentação Swagger estará disponível em:

```text
http://localhost:8000/docs
```

---

# 6. Executar a API com Kubernetes

**Antes de subir a api com kubernetes, suba o keycloak conforme descrito no readme do repositório** [sub-tech-challenge-3-auth](https://github.com/leonardobortolini/sub-tech-challenge-3-auth)

## 6.1 Inicializar o Minikube

```bash
minikube start
```

## 6.2 Utilizar o Docker interno do Minikube

Configure o terminal para utilizar o Docker interno do Minikube:

```bash
eval $(minikube docker-env)
```

## 6.3 Criar a imagem da API

```bash
docker build -t revenda-api:latest .
```

## 6.4 Aplicar os manifests

```bash
kubectl apply -f k8s/
```

Os manifests criam os recursos necessários para a API e seu banco de dados.

Verifique os pods:

```bash
kubectl get pods -n revenda
```

Verifique os serviços:

```bash
kubectl get svc -n revenda
```

---

# 7. Acessar a API no Kubernetes

Para acessar a API através do Minikube:

```bash
kubectl port-forward -n revenda service/revenda-api-service 18080:8000
```
A aplicação fica acessível no host em: http://localhost:18080

A documentação Swagger estará disponível em:

```text
/docs
```

Por exemplo:

```text
http://<URL>/docs
```

---

# Testes

O projeto possui testes automatizados utilizando Pytest.

Para executar os testes:

```bash
pytest
```

Resultado esperado:

```text
18 passed
```

Os testes cobrem principalmente:

- Validação de CPF
- Regras de negócio dos veículos
- Venda de veículos
- Prevenção de venda duplicada
- Tratamento de veículo inexistente
- Validação de CPF durante a venda
- Autorização baseada em roles

---

# CI — Integração Contínua

O projeto utiliza GitHub Actions para validação automática das alterações.

O pipeline de CI executa:

- Checkout do código
- Configuração do Python 3.12
- Instalação das dependências
- Execução dos testes automatizados
- Instalação do `yamllint`
- Validação dos manifests Kubernetes
- Validação do build da imagem Docker

As alterações são realizadas utilizando Pull Requests.

O CI é executado para Pull Requests e alterações nas branches:

- `dev`
- `main`

---

# CD — Deploy Contínuo

O projeto possui deploy automatizado utilizando GitHub Actions e Kubernetes.

O CD é executado após alterações nas branches:

- `dev`
- `main`

O pipeline:

1. Inicia um ambiente Minikube
2. Prepara o namespace Kubernetes
3. Configura o Docker interno do Minikube
4. Constrói a imagem da API
5. Aplica os manifests Kubernetes
6. Aguarda o PostgreSQL
7. Aguarda o deployment da API
8. Verifica os pods
9. Executa uma chamada ao endpoint `/health`

---

# Variáveis de ambiente

As configurações da aplicação são definidas através de variáveis de ambiente.

Utilize o arquivo:

```text
.env.example
```

como referência para criar o arquivo `.env`.

---

# CI/CD e Pull Requests

Todas as alterações do projeto devem passar pelo fluxo de desenvolvimento utilizando Pull Requests.

O fluxo adotado é:

```text
Feature Branch
      │
      ▼
Pull Request
      │
      ▼
CI
      │
      ├── Testes
      ├── Yamllint
      └── Docker Build
      │
      ▼
Merge
      │
      ▼
dev / main
      │
      ▼
CD
      │
      ▼
Kubernetes
```

Essa abordagem permite validar as alterações automaticamente antes da integração e realizar o deploy de forma automatizada.

---

# Observações

- O projeto Auth é uma aplicação independente da API e deve ser executado separadamente.
- O serviço Auth deve ser iniciado **antes da API** durante a execução local.
- Os usuários e roles utilizados pela aplicação são criados manualmente através da interface administrativa do Keycloak.
- A API utiliza o Keycloak exclusivamente para autenticação e autorização.
- Os dados relacionados aos usuários permanecem no serviço Auth.
- Os dados transacionais relacionados aos veículos, vendas e pagamentos permanecem no banco PostgreSQL da API.
- A API utiliza o `sub` presente no JWT para identificar o usuário durante a operação de compra.
