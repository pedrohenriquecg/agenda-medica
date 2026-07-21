# Agenda Médica

## Descrição

Agenda Médica é uma aplicação web desenvolvida com Flask que realiza a autenticação de usuários e exibe uma agenda de consultas médicas obtida por meio de uma API HTTP. Os usuários são armazenados em um banco de dados SQLite, e os agendamentos são apresentados em uma tabela utilizando a biblioteca Tabulator.

## Tecnologias utilizadas

- Python 3
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Tabulator
- Docker
- Docker Compose
- Pytest

## Executando o projeto com Docker

Clone o repositório:

```bash
git clone https://github.com/pedrohenriquecg/agenda-medica.git
cd agenda-medica
```

Construa e inicie a aplicação:

```bash
docker compose up -d --build
```

A aplicação estará disponível em:

```text
http://localhost:5000
```

Para interromper a execução:

```bash
docker compose down
```

## Credenciais do usuário de teste

**Usuário:** `admin`

**Senha:** `admin123`

## Exemplos de uso

1. Execute a aplicação utilizando Docker.
2. Acesse `http://localhost:5000`.
3. Faça login utilizando o usuário de teste.
4. Após a autenticação, a agenda médica será exibida.
5. Utilize o campo de pesquisa da tabela para localizar agendamentos por paciente, CPF ou médico.

## Decisões técnicas

- Desenvolvimento da aplicação utilizando Flask.
- Utilização do SQLite para armazenamento dos usuários.
- Armazenamento seguro das senhas utilizando hash com Werkzeug.
- Integração com a API de agendamentos por meio de requisições HTTP.
- Validação da estrutura da resposta da API antes da exibição dos dados.
- Organização do código em módulos para separar autenticação, acesso ao banco de dados e integração com a API.
- Utilização do Docker e Docker Compose para facilitar a execução da aplicação.
- Implementação de testes automatizados com Pytest.

## Limitações conhecidas

A aplicação utiliza uma API simulada para fornecer os dados dos agendamentos, conforme permitido pelo enunciado do desafio.