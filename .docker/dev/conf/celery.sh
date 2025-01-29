#!/bin/bash

DJANGODIR=/tyf/backend
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}
if [ -n "$NORELOAD" ]; then
	    PARAMS="--noreload"
fi

celery -A apps.celery_app purge -f &
celery -A apps.celery_app beat &
flower -A apps.celery_app --port=7999 &
celery -A apps.celery_app worker -c 2 -O fair