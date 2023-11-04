# Makefile for Code Formatting and Import Removal in Django Application

# Comandos
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
