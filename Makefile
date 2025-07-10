.PHONY: install lint test test-compose up down migrate

install:
	@if ! command -v uv &> /dev/null; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	uv sync --locked
	uv add black isort flake8

lint:
	black --check app
	isort --check-only app
	flake8 app

test-compose:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

test: test-compose

check: lint test-compose

up:
	docker-compose up -d --build

down:
	docker-compose down

migrate:
	docker-compose exec app alembic upgrade head