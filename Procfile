web: gunicorn requestbin.app:app --worker-class sanic.worker.GunicornWorker --max-requests 10000
release: python release.py