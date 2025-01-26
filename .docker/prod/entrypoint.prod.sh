#!/bin/sh

if [ "$DATABASE"="postgres" ]
then
    echo "Waiting for postgreSQL..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations categories collections comments follows media posts profiles registry tags users notifications chats
python manage.py migrate --no-input
python manage.py shell -c 'exec(open(\"apps/utils/load_data.py\").read())'
python manage.py collectstatic --no-input

exec "$@"