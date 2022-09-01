init:
	python3.7 -m venv .venv/
	poetry install
	direnv allow
