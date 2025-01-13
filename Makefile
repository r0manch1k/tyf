DOCKER_COMPOSE_DEV = docker-compose -f ./.docker/docker-compose.dev.yml
DOCKER_COMPOSE_PROD = docker-compose -f ./.docker/docker-compose.prod.yml

# development 
build-dev:
	$(DOCKER_COMPOSE_DEV) build

up-dev:
	$(DOCKER_COMPOSE_DEV) up -d

up-logs-dev:
	$(DOCKER_COMPOSE_DEV) up

down-dev:
	$(DOCKER_COMPOSE_DEV) down

migrate-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py migrate"

migrate-app-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py migrate $(app)"

createsuperuser-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py createsuperuser"

shell-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py shell"

makemigrations-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py makemigrations"

makemigrations-app-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend && python manage.py makemigrations $(app)"

startapp-dev:
	$(DOCKER_COMPOSE_DEV) exec backend bash -c "cd backend/apps && python ../manage.py startapp $(app)"

clean-dev:
	$(DOCKER_COMPOSE_DEV) down --rmi all

clean-volumes-dev:
	$(DOCKER_COMPOSE_DEV) down -v

# production 
build-prod:
	$(DOCKER_COMPOSE_PROD) build

up-prod:
	$(DOCKER_COMPOSE_PROD) up -d

up-logs-prod:
	$(DOCKER_COMPOSE_PROD) up

down-prod:
	$(DOCKER_COMPOSE_PROD) down

migrate-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py migrate"

createsuperuser-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py createsuperuser"

shell-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py shell"

makemigrations-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend && python manage.py makemigrations"

startapp-prod:
	$(DOCKER_COMPOSE_PROD) exec backend bash -c "cd backend/apps && python ../manage.py startapp $(app)"

clean-prod:
	$(DOCKER_COMPOSE_PROD) down --rmi all

clean-volumes-prod:
	$(DOCKER_COMPOSE_PROD) down -v

.PHONY: build-dev up-dev down-dev migrate-dev superuser-dev makemigrations-dev startapp-dev clean-dev clean-dev-volumes \
        build-prod up-prod down-prod migrate-prod superuser-prod makemigrations-prod startapp-prod clean-prod clean-prod-volumes
