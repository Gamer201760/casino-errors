.PHONY: test lint typecheck run pre-commit install

help:
	@echo "Доступные команды:"
	@echo "  make install      - Установить все зависимости"
	@echo "  make run          - Запустить casino"
	@echo "  make test         - Запустить тесты pytest"
	@echo "  make lint         - Запустить линтер ruff"
	@echo "  make typecheck    - Запустить проверку типов mypy"
	@echo "  make pre-commit   - Запустить все проверки (lint, typecheck, test)"

install:
	uv sync

make run:
	uv run main.py

test:
	uv run pytest -v

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

pre-commit: lint typecheck test
