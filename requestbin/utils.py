import psycopg2
import ujson
import urllib.parse as urlparse

from functools import wraps
from gevent.socket import wait_read, wait_write
from inspect import isawaitable
from psycopg2 import extensions

from sanic.response import BaseHTTPResponse


def cors(origin=None):
    CORS_HEADERS = {
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Origin": "*",
    }

    def decorator(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            response = fn(*args, **kwargs)
            if isinstance(response, BaseHTTPResponse):
                response.headers.update(CORS_HEADERS)
                return response
            elif isawaitable(response):

                async def make_cors():
                    r = await response
                    r.headers.update(CORS_HEADERS)
                    return r

                return make_cors()
            return response

        return wrap

    return decorator


def make_psycopg_green():
    """ Configure Psycopg to be used with gevent in non-blocking way.
    """
    if not hasattr(extensions, "set_wait_callback"):
        raise ImportError(
            "support for coroutines not available in this Psycopg version (%s)"
            % psycopg2.__version__
        )

    extensions.set_wait_callback(psycopg_gevent_wait_callback)


def psycopg_gevent_wait_callback(conn, timeout=None):
    """A wait callback useful to allow gevent to work with Psycopg."""
    while True:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            wait_read(conn.fileno(), timeout=timeout)
        elif state == extensions.POLL_WRITE:
            wait_write(conn.fileno(), timeout=timeout)
        else:
            raise psycopg2.OperationalError("Bad result from poll: %r" % state)
