web: gunicorn core.wsgi --bind 0.0.0.0:$PORT
worker: celery -A core worker -l info
