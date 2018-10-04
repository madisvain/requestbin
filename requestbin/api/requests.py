from sanic import Blueprint
from sanic.response import json

from requestbin.models import Bin, Request
from requestbin.schemas import RequestSchema


requests = Blueprint("requests", url_prefix="/api/requests")


@requests.route("/", methods=["GET"])
async def list_view(request):
    requests = (
        Request.select()
        .join(Bin)
        .where(
            (Bin.session == request.cookies.get("session")) |
            (Bin.secret == request.raw_args.get("secret", ""))
        )
        .order_by(Request.created_at.desc())
    )
    if "bin" in request.raw_args:
        requests = requests.filter(bin=request.raw_args["bin"])
    return json(RequestSchema(many=True).dump(requests))


@requests.route("/<uuid>", methods=["GET"])
async def detail_view(request, uuid):
    request = Request.get(Request.id == uuid)
    return json(RequestSchema().dump(request))


@requests.route("/<uuid>", methods=["DELETE"])
async def delete_view(request, uuid):
    try:
        Request.get(Request.id == uuid).delete_instance()
        return json("", status=200)
    except Request.DoesNotExist:
        return json("", status=410)
