#!/bin/sh

until cd /app/backend/converter
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A converter worker --loglevel=info --concurrency 1 -E

