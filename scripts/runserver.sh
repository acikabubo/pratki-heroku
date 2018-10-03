# flask run --host 0.0.0.0 --port 5000 --reload
gunicorn app:app -b 0.0.0.0:5000 --certfile server.crt --keyfile server.key --preload --workers 1 --timeout 100 --log-file=-
