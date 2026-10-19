# Circuito API — Gestão de Campeonato de F1

API REST para gerenciar um campeonato de Fórmula 1: equipes, pilotos, corridas e resultados.
Projeto da disciplina de Cloud Computing, com foco em **CI/CD**: testes automatizados,
containerização com Docker e deploy automático na AWS.

## Tecnologias

- Python 3.11, FastAPI, SQLAlchemy
- PostgreSQL 16 (produção) e SQLite (testes)
- Docker e Docker Compose
- Pytest e Flake8
- GitLab CI/CD, GitLab Container Registry
- AWS EC2 (Ubuntu)

## Arquitetura

```
git push (main) -> GitLab CI/CD -> imagem Docker -> GitLab Container Registry
                                                  -> deploy via SSH -> AWS EC2
                                                       (API + PostgreSQL em containers)
```

## Como rodar com Docker

```bash
git clone https://github.com/KBerliet/circuito-api.git
cd circuito-api
docker compose up --build
```

A API fica em `http://localhost:8000` e a documentação interativa em `http://localhost:8000/docs`.

> A senha do PostgreSQL no `docker-compose.yml` é apenas um valor de exemplo para
> desenvolvimento. Em produção, use variáveis de ambiente.

## Como rodar sem Docker

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Sem a variável `DATABASE_URL`, a aplicação usa SQLite local.

## Testes e lint

```bash
pytest -v
flake8 app tests
```

São 32 testes cobrindo sucesso, erros de validação (400/422) e recurso não encontrado (404).

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /health | Healthcheck |
| POST / GET | /teams | Cria / lista equipes |
| GET | /teams/{id} | Busca equipe |
| POST / GET | /drivers | Cria / lista pilotos |
| GET | /drivers/{id} | Busca piloto |
| POST / GET | /races | Cria / lista corridas |
| GET | /races/{id} | Busca corrida |
| POST / GET | /results | Registra / lista resultados |
| GET | /results/race/{id} | Resultados de uma corrida |

## Pipeline de CI/CD

Definido em `.gitlab-ci.yml` (o pipeline roda no GitLab, não no GitHub):

1. **build**: instala as dependências
2. **test**: roda o pytest
3. **lint**: roda o flake8
4. **docker-build**: constrói a imagem Docker
5. **docker-push**: publica a imagem no GitLab Container Registry
6. **deploy**: atualiza os containers na instância EC2 via SSH

Os estágios 4 a 6 rodam apenas na branch `main`. Credenciais ficam em variáveis protegidas de CI/CD.

## Observação

Parte do código foi desenvolvida com apoio de IA (Claude). Todo o processo de execução, teste,
depuração e deploy foi realizado manualmente pelo autor.