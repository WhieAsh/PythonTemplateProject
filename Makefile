.PHONY: start start_build stop unit_tests

start:
	docker-compose up -d

start_build:
	docker-compose up --build -d

stop:
	docker-compose down

unit_tests:
	docker-compose exec -T app-test  pytest tests

check_lint:
	docker-compose exec app-test mypy . && isort --check-only . $$ black --check app

fix_lint:
	docker-compose exec app-test isort . $$ black app