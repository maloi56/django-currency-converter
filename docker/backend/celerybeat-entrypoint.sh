#!/bin/sh

until cd /app/backend/converter
do
    echo "Waiting for server volume..."
done

# run a celerybeat :)

celery -A converter beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
