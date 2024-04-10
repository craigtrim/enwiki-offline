# ----------------------------------------------------------------
# enwiki-local
# ----------------------------------------------------------------

install:
	@echo Installing Microservice
	poetry lock
	poetry check
	poetry update
	poetry install

test:
	@echo Unit Testing Microservice
	poetry run pytest --disable-pytest-warnings

build:
	@echo Building Microservice
	make install
	make test
	poetry build

freeze:
	@echo Freezing Requirements
	poetry run pip freeze > requirements.txt
	poetry run python -m pip install --upgrade pip

all:
	make build
	make freeze

# ----------------------------------------------------------------
# (Optional) Linting -- Compatible with Python 3.9+
#
activate:
	@echo Activating Microservice
	poetry run pre-commit autoupdate
	poetry run pre-commit install

linters:
	@echo Running Linters
	poetry run pre-commit run --all-files
# ----------------------------------------------------------------
