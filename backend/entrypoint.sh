#!/bin/bash
set -e

echo "Waiting for MySQL..."
while ! python -c "
import MySQLdb
try:
    MySQLdb.connect(
        host='${MYSQL_HOST:-mysql}',
        port=int('${MYSQL_PORT:-3306}'),
        user='${MYSQL_USER:-docsuser}',
        passwd='${MYSQL_PASSWORD:-docspass}',
        db='${MYSQL_DATABASE:-docs_cure_db}'
    )
    print('MySQL is ready!')
except Exception as e:
    print(f'MySQL not ready: {e}')
    exit(1)
" 2>/dev/null; do
    echo "MySQL not ready, retrying in 2s..."
    sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-4}" \
    --threads "${GUNICORN_THREADS:-2}" \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile -
