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
	poetry run pytest --disable-pytest-warnings

build:
	make install
	make test
	poetry build

freeze:
	poetry run pip freeze > requirements.txt
	poetry run python -m pip install --upgrade pip

all:
	make build
	make freeze

# ----------------------------------------------------------------
# (Optional) Linting -- Compatible with Python 3.9+
#
activate:
	poetry run pre-commit autoupdate
	poetry run pre-commit install

linters:
	poetry run pre-commit run --all-files
# ----------------------------------------------------------------
