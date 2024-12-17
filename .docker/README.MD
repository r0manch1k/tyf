## Before developing do the following:

1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`

---

## Instructions for starting development (initial setup)

1. build all containers (django, postgres, redis): 
`docker-compose -f ./.docker/docker-compose.dev.yml build`

2. run containers: 
`docker-compose -f ./.docker/docker-compose.dev.yml up -d` (flag -d for running without terminal logs)

3. run migrate: 
`docker-compose -f ./.docker/docker-compose.dev.yml exec tyg_backend python manage.py migrate`

4. create superuser: 
`docker-compose -f ./.docker/docker-compose.dev.yml exec tyg_backend python manage.py createsuperuser`

5. stop containers: 
`docker-compose -f ./.docker/docker-compose.dev.yml down`

---

## Instructions for development (after initial setup)

#### Docker start/stop commands

You can use Docker Desktop to manage containers or run this commands in terminal:

- run containers (run server (localhost:8000), database (localhost:5432) and redis (localhost:6379)): 
`docker-compose -f ./.docker/docker-compose.dev.yml up -d` (flag -d for running without terminal logs)

- stop containers: 
`docker-compose -f ./.docker/docker-compose.dev.yml down`

- delete all containers: 
`docker-compose -f ./.docker/docker-compose.dev.yml down --rmi all`

- delete database data: 
`docker-compose -f ./.docker/docker-compose.dev.yml down -v`

#### Django commands

- run migrate: 
`docker-compose -f ./.docker/docker-compose.dev.yml exec tyg_backend python manage.py migrate`

- make migrations: 
`docker-compose -f ./.docker/docker-compose.dev.yml exec tyg_backend python manage.py makemigrations`

- create superuser: 
`docker-compose -f ./.docker/docker-compose.dev.yml exec tyg_backend python manage.py createsuperuser`

- create new app: 
`docker-compose -f ./.docker/docker-compose.dev.yml exec tyg_backend python manage.py startapp <app_name>`

---

## Instructions for production

1. build all containers (run server, database, redis): 
`docker-compose -f ./.docker/docker-compose.prod.yml build`

2. run containers: 
`docker-compose -f ./.docker/docker-compose.prod.yml up -d` (flag -d for running without terminal logs)

3. make migrations: 
`docker-compose -f ./.docker/docker-compose.prod.yml exec tyg_backend python manage.py makemigrations`

4. migrate: 
`docker-compose -f ./.docker/docker-compose.prod.yml exec tyg_backend python manage.py migrate`

5. create superuser: 
`docker-compose -f ./.docker/docker-compose.prod.yml exec tyg_backend python manage.py createsuperuser`

6. stop containers: 
`docker-compose -f ./.docker/docker-compose.prod.yml down`

(and other commands from development section, but use `docker-compose.prod.yml` instead of `docker-compose.dev.yml`)
