#!/bin/bash

bash -c "cd backend && python manage.py makemigrations categories collections comments follows media posts profiles registry tags users notifications chats"
bash -c "cd backend && python manage.py migrate"
bash -c "cd backend && python manage.py load_data"
bash -c "cd backend && python manage.py collectstatic --no-input"

NAME="tyf"
DJANGO_NUM_WORKERS=2
DJANGODIR=/tyf/backend/
DJANGO_ASGI_MODULE=tyf.asgi
WORKER_CLASS=uvicorn.workers.UvicornWorker

cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

gunicorn ${DJANGO_ASGI_MODULE} \
  --preload \
  --pythonpath ${PYTHONPATH} \
  --name ${NAME} \
  --workers ${DJANGO_NUM_WORKERS} \
  --worker-class ${WORKER_CLASS} \
  --max-requests 3000 \
  --max-requests-jitter 1500 \
  --bind 0.0.0.0:8080 \
  --log-level info \
  --log-file - \
  --pid gunicorn.pid
