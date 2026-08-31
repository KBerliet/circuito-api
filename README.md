# Circuito API — Gestão de Campeonato de F1

API REST para gerenciar um campeonato de Fórmula 1: equipes, pilotos, corridas e resultados.

Projeto da disciplina de Cloud Computing — Fase 1 (Versionamento e Integração Contínua).

## Descrição

A API representa um domínio único e coerente — a gestão de um campeonato de F1:

- **Equipes (`/teams`)** — cadastro das escuderias da temporada
- **Pilotos (`/drivers`)** — cadastrados e vinculados a uma equipe
- **Corridas (`/races`)** — etapas do calendário
- **Resultados (`/results`)** — classificação de um piloto em uma corrida, com posição e pontos

## Tecnologias utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- SQLite (banco de dados relacional usado em desenvolvimento e testes)
- Pytest (testes automatizados)
- Flake8 (lint)
- GitLab CI/CD

## Como rodar o projeto localmente

```bash
# clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd f1-cicd-project

# criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# instalar as dependências
pip install -r requirements.txt

# rodar a aplicação
uvicorn app.main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

## Rodando os testes

```bash
pytest -v
```

## Rodando o lint

```bash
flake8 app tests
```

## Endpoints

| Método | Rota                    | Descrição                                        |
| ------ | ----------------------- | ------------------------------------------------ |
| GET    | /health                 | Healthcheck da aplicação                         |
| POST   | /teams                  | Cria uma equipe                                  |
| GET    | /teams                  | Lista todas as equipes                           |
| GET    | /teams/{id}             | Busca uma equipe por id                          |
| POST   | /drivers                | Cria um piloto (vinculado a uma equipe)          |
| GET    | /drivers                | Lista todos os pilotos                           |
| GET    | /drivers/{id}           | Busca um piloto por id                           |
| POST   | /races                  | Cria uma corrida                                 |
| GET    | /races                  | Lista todas as corridas                          |
| GET    | /races/{id}             | Busca uma corrida por id                         |
| POST   | /results                | Registra o resultado de um piloto em uma corrida |
| GET    | /results                | Lista todos os resultados                        |
| GET    | /results/race/{race_id} | Lista os resultados de uma corrida específica    |

## Pipeline de CI

O `.gitlab-ci.yml` roda automaticamente a cada push e a cada Merge Request, com 3 estágios:

1. **build** — instala as dependências
2. **test** — executa os 32 testes automatizados com pytest
3. **lint** — valida o estilo do código com flake8
