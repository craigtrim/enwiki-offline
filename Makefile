# ----------------------------------------------------------------
# enwiki-local
# ----------------------------------------------------------------

install:
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
# (Optional) 	Linting
#				Compatible with Python 3.9 and higher
#
activate:
	poetry run pre-commit autoupdate
	poetry run pre-commit install

linters:
	poetry run pre-commit run --all-files
# ----------------------------------------------------------------


# ----------------------------------------------------------------
# (Optional) 	Machine Specific Commands
#				These Commands can be modified for local environments
#
parse:
	mkdir -p resources/enwiki
	poetry run python drivers/parse_enwiki_all_titles.py /Users/craigtrim/Desktop/enwiki-20240301-all-titles
# ----------------------------------------------------------------
