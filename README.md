# TRABALHO SUBSTITUTIVO DE TECH CHALLENGE - FASE 2

A aplicação permite o cadastro e gerenciamento de veículos disponíveis para venda, controle das vendas realizadas e integração com um sistema externo de pagamentos através de webhook.

- Tecnologias utilizadas
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- Kubernetes
- Minikube

## Arquitetura do projeto

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
│   └── database
│
└── apresentacao
    └── controllers
```

## Camadas

### Domínio
Regras principais do negócio, entidades, validações e exceções.

### Aplicação
Casos de uso responsáveis por executar as operações do sistema.

### Infraestrutura
Detalhes externos da aplicação, como conexão com banco de dados e implementação dos repositórios.

### Apresentação
Controllers responsáveis pela exposição dos endpoints da API.

## Funcionalidades
- Cadastro de veículos
- Alteração de veículos cadastrados
- Listagem de veículos disponíveis ordenados pelo menor preço
- Venda de veículos
- Validação de CPF do comprador
- Listagem de veículos vendidos ordenados pelo menor preço
- Controle de status do pagamento
- Webhook para atualização de pagamento

## Executando com Docker Compose
### Pré-requisitos
- Docker
- Docker Compose
- Subir aplicação

Na raiz do projeto execute:

docker compose up --build

Após inicializar, acesse:

http://localhost:8000/docs

O Swagger estará nesse endereço.

## Executando com Kubernetes (Minikube)
### Pré-requisitos
- Docker
- Kubectl
- Minikube

### Inicializar Minikube
minikube start

### Criar imagem da API no Minikube

Configurar o terminal para usar o Docker interno do Minikube:

eval $(minikube docker-env)

Criar a imagem:

docker build -t revenda-api:latest .

### Aplicar os manifestos Kubernetes

Executar:

kubectl apply -f k8s/

Serão criados:

- Namespace
- ConfigMap
- Secret
- Deployment da API
- Deployment do PostgreSQL
- Service da API
- Service do PostgreSQL

## Validar recursos Kubernetes

kubectl get pods -n revenda

kubectl get svc -n revenda

## Acessar aplicação no Kubernetes

Execute:

minikube service revenda-api-service -n revenda

Será disponibilizada uma URL. Acesse /docs para acessar o Swagger

## Principais endpoints

### Veículos

Cadastrar veículo:

POST /veiculos

Editar veículo:

PUT /veiculos/{id}

Listar veículos disponíveis:

GET /veiculos/disponiveis

Listar veículos vendidos:

GET /veiculos/vendidos

Realizar venda:

POST /veiculos/{id}/vender

### Pagamentos

Atualizar pagamento via webhook:

POST /pagamentos/webhook

Consultar pagamentos por status:

GET /pagamentos?status=STATUS

### Status de pagamento

Os pagamentos podem possuir os seguintes status:

PENDENTE | APROVADO | CANCELADO