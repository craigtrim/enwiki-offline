# ----------------------------------------------------------------
# baseblock
# ----------------------------------------------------------------

ifeq ($(OS),Windows_NT)
    os_shell := powershell
	copy_setup := resources/scripts/copy_setup.ps1
else
    os_shell := $(SHELL)
	copy_setup := resources/scripts/copy_setup.sh
endif

copy_setup:
	$(os_shell) $(copy_setup)

# ----------------------------------------------------------------

install:
	@echo Installing Microservice
	poetry lock
	poetry check
	poetry update
	poetry install
	poetry run pre-commit install

activate:
	@echo Activating Microservice
	poetry run pre-commit autoupdate

test:
	echo Unit Testing Microservice
	poetry run pytest --disable-pytest-warnings

build:
	@echo Building Microservice
	make install
	make test
	poetry build
	make copy_setup

linters:
	@echo Running Linters
	poetry run pre-commit run --all-files
#	20230116; breaks on cartesian-* methods
#	poetry run flakeheaven lint

freeze:
	@echo Freezing Requirements
	poetry run pip freeze > requirements.txt
	poetry run python -m pip install --upgrade pip

all:
	make build
	make linters
	make freeze
	make copy_setup
