gunicorn --workers 2 --bind 0.0.0.0:8000 flask_app:app > /dev/null 2>&1
