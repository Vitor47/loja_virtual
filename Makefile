# Makefile for Code Formatting and Import Removal in Django Application

# Configuração
PYTHON = python3.10
DJANGO_MANAGE = python manage.py

# Comandos
install-dependencies:
	pip install -r requirements.txt

makemigrations:
	$(DJANGO_MANAGE) makemigrations

migrate:
	$(DJANGO_MANAGE) migrate

runserver:
	$(DJANGO_MANAGE) runserver

create-superuser:
	$(DJANGO_MANAGE) createsuperuser

shell:
	$(DJANGO_MANAGE) shell

format:
	black .
	isort -rc .

remove-unused-imports:
	autoflake --remove-all-unused-imports -i -r .

# Linting e Checagem
lint:
	flake8 .
	mypy .
	pylint .

# Regras predefinidas
.PHONY: format remove-unused-imports lint
