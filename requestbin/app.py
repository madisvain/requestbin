import os
import secrets
import shortuuid
import sys
import uuid

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


""" Website
"""


@app.route("/", methods=["GET", "HEAD"])
async def index(request):
    if request.method == "HEAD":
        return html("")
    return await file("./requestbin/web/index.html")


# Static content
app.static("/index.html", "./requestbin/web/")
app.static("/", "./requestbin/web/", pattern=r".*?\.(?:js|css)$")
app.static("/static/", "./requestbin/web/static")
app.static("/favicon.ico", "./requestbin/web/favicon.ico")
app.static("/robots.txt", "./requestbin/web/robots.txt")


""" Requestbin
"""


@app.route("/<suuid:string>", methods=HTTP_METHODS)
async def requestbin(request, suuid):
    if len(suuid) == 22:
        b = Bin.get(Bin.id == shortuuid.decode(suuid))
        r = Request.create(
            bin=b,
            method=request.method,
            headers=dict(request.headers),
            json=dict(request.json),
            args=dict(request.args),
            form=dict(request.form),
            body=request.body,
            ip=request.ip,
            port=request.port,
            time=0,
            size=sys.getsizeof(request.body),
        )
        return text("ok\n", status=200)
    return text("not found\n", status=404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, access_log=False, debug=True)
