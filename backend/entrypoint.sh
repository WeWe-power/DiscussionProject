#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py collectstatic
python manage.py makemigrations forum
python manage.py migrate forum
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser \
        --username admin \
        --name admin \
        --email admin@gmail.com \
        --noinput

exec "$@"