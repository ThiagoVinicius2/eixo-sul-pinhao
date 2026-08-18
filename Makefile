.PHONY: setup seed test lint run
setup:
	python -m pip install -e ".[dev]" ruff mypy pytest
seed:
	python -m pinhao.db.seed
test:
	pytest -q
lint:
	ruff check . && ruff format --check . && mypy
run:
	python -m pinhao
