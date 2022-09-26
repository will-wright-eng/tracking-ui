#* Variables
SHELL := /usr/bin/env bash
PYTHON := python3
PYTHONPATH := `pwd`

#* Docker variables
IMAGE := tracking_ui
VERSION := latest

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

.DEFAULT_GOAL := help

help: ## list make commands
	@echo ${MAKEFILE_LIST}
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## initalize project -- install poetry and pre-commit
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -
	pre-commit install

run-app: ## run app from poetry env var
	poetry run python -m tracking_ui

dc-up: ## build and start docker compose app
	docker-compose -f deploy/docker-compose.yml --project-directory . up --build

dc-up-dev: ## start docker compose dev app
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up

dc-test: ## run tests from docker compose
	docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
	docker-compose -f deploy/docker-compose.yml --project-directory . down

dc-test-kill: ## kill docker compose tests
	docker-compose -f deploy/docker-compose.yml --project-directory . down


install: ## old list
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n
	#poetry run mypy --install-types --non-interactive ./

pre-commit-install: ## old list
	poetry run pre-commit install

codestyle: ## old list
	poetry run pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
# 	poetry run black --config pyproject.toml ./

# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
docker-build: ## old list
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
docker-remove: ## old list
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)
