release: python manage.py migrate
web: daphne Notychat.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=Notychat.settings -v2