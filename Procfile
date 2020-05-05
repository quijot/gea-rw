release: python manage.py makemigrations gea && python manage.py migrate
web: gunicorn estudio.wsgi --log-file -
