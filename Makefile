test:
	poetry run pytest --capture=no --cov=acac --cov-report=term-missing

init:
	python3.7 -m venv .venv/
	poetry install
	direnv allow
