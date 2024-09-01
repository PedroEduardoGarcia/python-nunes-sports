# Nunes Sports Full Simple Stack API
[![AWS](https://img.shields.io/badge/AWS-Cloud-yellow.svg)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12-blue.svg)](https://www.postgresql.org/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9-blue.svg)](https://www.typescriptlang.org/)

## Acessar a Aplicação

O projeto está hospedado na aws, segue o link:
   
[**Nunnes Sports**](http://nunes-sports-frontend-bucket.s3-website-us-east-1.amazonaws.com/)

[**http://nunes-sports-frontend-bucket.s3-website-us-east-1.amazonaws.com/**](http://nunes-sports-frontend-bucket.s3-website-us-east-1.amazonaws.com/)

## Descrição do Projeto

O projeto **python-nunes-sports** é uma aplicação web desenvolvida para atender ao requisito de um cliente fictício. O sistema permite a exibição, criação, edição e deleção de produtos. O objetivo principal é mostrar a crição da aplicação com frontend, backend e banco de dados com deploy na AWS, aplicando conceitos de Clean Code, SOLID e boas práticas de desenvolvimento. O frontend está servido em bucket s3 e o backend dockerizado em um ec2.

## Requisitos

1. **Base de Dados:**
   - A aplicação utiliza uma base de dados com uma tabela `produtos` contendo os seguintes campos:
     - id do produto
     - Nome do produto
     - Código do produto
     - Descrição do produto
     - Preço do produto
     - data de criação

2. **Funcionalidades da Página Web:**
   - **Exibição dos Produtos:** A página deve mostrar uma tabela com todos os produtos disponíveis na base de dados.
   - **Criação de Produtos:** Permitir a adição de novos produtos à base de dados.
   - **Edição de Produtos:** Permitir a modificação das informações de produtos existentes.
   - **Deleção de Produtos:** Permitir a remoção de produtos da base de dados.
   - Todas as ações realizadas na página web refletem diretamente na base de dados.

## Tecnologias Utilizadas

- **Backend:** FastAPI para construção da API.
- **Frontend:** React para a interface web.
- **Banco de Dados:** PostgreSQL para armazenar os dados dos produtos.
- **Docker:** Para criar um ambiente de desenvolvimento isolado e facilitar o deploy.
- **Docker Compose:** Para orquestrar os contêineres do backend e do banco de dados.


## Como Executar o Projeto

1. **Configuração do Ambiente:**
   - Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2. **Iniciar o Projeto:**
   - Navegue até a raiz do projeto e execute o seguinte comando para iniciar os contêineres:
     ```bash
     docker-compose up
     ```
   - Isso iniciará o backend e o banco de dados, e a aplicação estará acessível em `http://localhost:3000`.

   Da mesma forma é possível rodar npm build para montar o frontend.

## Outros comandos:

Para rodar o backend:
```bash
docker compose up -d
```

Para desligar o backend:
```bash
docker compose down -d
```

Para testar a rota do backend:
```bash
curl -X POST "http://localhost:3000/api/hello_test" -H "Content-Type: application/json" -d '{"username": "JohnDoe"}'
```

Para testes unitários rodar:
```bash
docker-compose exec backend pytest -v tests/
```

## Author

[**Pedro Eduardo Garcia - Github**](https://github.com/PedroEduardoGarcia)

[**Pedro Eduardo Garcia - Linkedin**](https://www.linkedin.com/in/pedro-eduardo-garcia-766774244/)