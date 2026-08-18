.PHONY: up down seed test-api test-web lint-api lint-web build-web verify

up:
	docker compose up --build

down:
	docker compose down

seed:
	cd apps/api && python scripts/seed_mock.py

test-api:
	cd apps/api && python -m pytest

test-web:
	cd apps/web && pnpm test

lint-api:
	cd apps/api && ruff check .

lint-web:
	cd apps/web && pnpm lint

build-web:
	cd apps/web && pnpm build

verify: test-api test-web lint-api lint-web build-web
