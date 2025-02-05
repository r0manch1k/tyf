DOCKER_COMPOSE_DEV = docker-compose -f ./.docker/docker-compose.dev.yml
DOCKER_COMPOSE_PROD = docker-compose -f ./.docker/docker-compose.prod.yml -p tyf

# For development 
build-dev:
	$(DOCKER_COMPOSE_DEV) build

# For development 
build-beat-dev:
	$(DOCKER_COMPOSE_DEV) build beat	

# For development 
up-dev:
	$(DOCKER_COMPOSE_DEV) up -d

# For development 
up-logs-dev:
	$(DOCKER_COMPOSE_DEV) up

# For development 
down-dev:
	$(DOCKER_COMPOSE_DEV) down

# For development 
migrate-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py migrate"

# For development 
migrate-app-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py migrate $(app)"

# For development 
createsuperuser-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py createsuperuser"

# For development 
shell-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py shell"

# For development 
makemigrations-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py makemigrations"

# For development 
makemigrations-app-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py makemigrations $(app)"

# For development 
startapp-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend/apps && python ../manage.py startapp $(app)"

# For development 
clean-dev:
	$(DOCKER_COMPOSE_DEV) down --rmi all

# For development 
clean-volumes-dev:
	$(DOCKER_COMPOSE_DEV) down -v

# For development 
load-csv-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py load_data"

# For development 
create-api-key-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py create_api_key"


# For production
build-prod:
	$(DOCKER_COMPOSE_PROD) build

# For production
up-prod:
	$(DOCKER_COMPOSE_PROD) up -d

# For production
up-logs-prod:
	$(DOCKER_COMPOSE_PROD) up

# For production
down-prod:
	$(DOCKER_COMPOSE_PROD) down

# For production
migrate-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py migrate"

# For production
createsuperuser-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py createsuperuser"

# For production
shell-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py shell"

# For production
makemigrations-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py makemigrations"

# For production
startapp-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend/apps && python ../manage.py startapp $(app)"

# For production
clean-prod:
	$(DOCKER_COMPOSE_PROD) down --rmi all

# For production
clean-volumes-prod:
	$(DOCKER_COMPOSE_PROD) down -v

# For production
load-csv-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py load_data"

# For production
create-api-key-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py create_api_key"

# For production
run-load-test-app:
	locust -f ./.docker/prod/loadtest/locustfile.py

.PHONY: build-dev up-dev down-dev migrate-dev superuser-dev makemigrations-dev startapp-dev clean-dev clean-dev-volumes load-csv-dev create-api-key-dev\
        build-prod up-prod down-prod migrate-prod superuser-prod makemigrations-prod startapp-prod clean-prod clean-prod-volumes load-csv-prod create-api-key-prod
