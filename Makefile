test:
	poetry run pytest --capture=no --cov=acac --cov-report=term-missing

switch:
	git switch --create develop

after-develop-merged:
	git switch main
	git pull --prune
	git branch --delete develop
	make switch

init:
	python3.7 -m venv .venv/
	poetry install
	direnv allow

editable-install:
	/usr/local/bin/python3.9 -m pip install --editable .
