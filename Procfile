release: python manage.py migrate
web: gunicorn estudio.wsgi --workers 2 --timeout 120 --log-file -
