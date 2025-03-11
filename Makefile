.PHONY: run install update-deps create-venv activate-venv run-redis run-celery run-services

run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

install:
	pip install -r requirements.txt

update-deps:
	pip freeze > requirements.txt

create-venv:
	python3 -m venv venv

activate-venv:
	@echo "To activate the virtual environment, run:"
	@echo "source venv/bin/activate"

# Start Redis server (requires Redis to be installed)
run-redis:
	redis-server

# Start Celery worker
run-celery:
	celery -A app.celery_app worker --loglevel=info

# Start server, Redis, and Celery workers
run-services:
	@echo "Starting agent server"
	@uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
	@echo "Starting Redis server..."
	@redis-server --daemonize yes
	@echo "Starting Celery worker..."
	@celery -A app.celery_app worker --loglevel=info
