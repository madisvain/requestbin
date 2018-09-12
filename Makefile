run:
	pipenv run gunicorn requestbin.app:app -b 127.0.0.1:5000 --worker-class sanic.worker.GunicornWorker --workers 2 --reload

test:
	pipenv run pytest -s --ignore=requestbin/web