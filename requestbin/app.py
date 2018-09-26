import os
import secrets
import shortuuid
import sys
import time
import uuid

from peewee import DoesNotExist
from sanic import Sanic
from sanic.constants import HTTP_METHODS
from sanic.response import file, json, html, text

from raven.contrib.sanic import Sentry

from requestbin import api
from requestbin.models import db, Bin, Request
from requestbin.utils import cors, make_psycopg_green

SITE_URL = "http://localhost:8000"


app = Sanic()
# Sentry
sentry = Sentry(app)

# API
app.blueprint(api.bins)
app.blueprint(api.requests)


@app.listener("before_server_start")
async def initialize(app, loop):
    # Check that tables exist
    db.create_tables(models=[Bin, Request])
    make_psycopg_green()


""" Middleware
"""


@app.middleware("response")
async def session(request, response):
    cookie = request.cookies.get("session")
    if not cookie:
        response.cookies["session"] = secrets.token_hex(32)


@app.middleware("request")
async def add_start_time(request):
    request["start_time"] = time.time()


""" Requestbin
"""


@app.route("/<suuid:.{22}>", methods=HTTP_METHODS)
async def requestbin(request, suuid):
    bin_id = shortuuid.decode(suuid)
    try:
        b = Bin.get(Bin.id == bin_id)
    except DoesNotExist:
        return text("not found\n", status=404)

    Request.create(
        bin=b,
        method=request.method,
        headers=dict(request.headers),
        json=dict(request.json) if request.json else dict(),
        args=dict(request.args),
        form=dict(request.form),
        body=request.body,
        ip=request.ip,
        port=request.port,
        time=round((time.time() - request["start_time"]) * 1000),
        size=sys.getsizeof(request.body),
    )
    return text("ok\n", status=200)


""" Static
"""


app.static("/", "./requestbin/web/", pattern=r".*?\.(?:js|css)$")
app.static("/static/", "./requestbin/web/static")
app.static("/favicon.ico", "./requestbin/web/favicon.ico")
app.static("/robots.txt", "./requestbin/web/robots.txt")



""" Website
"""

@app.route("/", methods=["GET", "HEAD"])
@app.route("/<path:string>", methods=["GET", "HEAD"])
@app.route("/<path:string>/<subpath:string>", methods=["GET", "HEAD"])
async def index(request, path=None, subpath=None):
    if request.method == "HEAD":
        return html("")
    return await file("./requestbin/web/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, access_log=False, debug=True)
