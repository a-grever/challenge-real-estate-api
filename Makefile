.PHONY : fmt migration import-data lint test lint-docker test-docker

fmt:
	black ./app ./tests
	isort ./app ./tests

lint:
	black --check ./app ./tests
	isort --check ./app ./tests
	flake8 ./app ./tests
	mypy ./app ./tests

test:
	pytest

migration:
	alembic upgrade head

import-data:
	docker-compose run --rm -e RABBIT_MQ_HOST=rabbitmq backend python tests/publish_events.py

lint-docker:
	docker-compose run --rm backend make lint

test-docker:
	docker-compose run --rm backend sh -c "sleep 5 && make test"
