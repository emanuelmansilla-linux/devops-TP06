# DevOps Portfolio — TP07: CI/CD
![CI/CD Pipeline](https://github.com/emanuelmansilla/devops-TP06/actions/workflows/cicd.yml/badge.svg)

App de notas con pipeline CI/CD completo usando GitHub Actions.

## Pipeline
| Stage | Trigger | Qué hace |
| --- | --- | --- |
| lint | todo push | flake8 en Python, yamllint en YAML |
| test | después de lint | pytest con reporte de cobertura |
| build-push | main y develop | docker buildx, push a Docker Hub |
| deploy | solo main | SSH al servidor, compose pull + up |

## Secrets requeridos
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_SSH_KEY`

## Correr tests localmente
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --cov=. --cov-report=term-missing
```
