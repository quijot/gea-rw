release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn estudio.wsgi --workers 2 --timeout 120 --log-file -
