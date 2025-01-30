#!/bin/bash

DJANGODIR=/tyf/backend
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}
if [ -n "$NORELOAD" ]; then
	    PARAMS="--noreload"
fi

celery -A apps.celery_app purge -f &
celery -A apps.celery_app beat &
celery -A apps.celery_app worker -c 2 -O fair