test:
	poetry run pytest --capture=no --cov=acac --cov-report=term-missing

switch:
	git switch --create develop

after-develop-merged:
	git switch main
	git pull --prune
	git branch --delete develop
	make switch

clean:
	rm -r .pytest_cache/
	rm -r .venv/
	rm .coverage

init:
	python3.7 -m venv .venv/
	poetry install
	direnv allow
	pnpm install

editable-install:
	/usr/local/bin/python3.7 -m pip install --editable .
