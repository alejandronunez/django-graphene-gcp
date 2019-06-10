#!/bin/bash

echo >&2 "Waiting for mysql..."
dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout 1m

echo >&2 "Waiting for ES..."
dockerize -wait ELASTICSEARCH_CONNECTION_STRING -timeout 1m

echo >&2 "Running migrations..."
python manage.py migrate

echo >&2 "Creating index..."
python manage.py search_index --create > /dev/null

exec "$@"