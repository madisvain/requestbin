import shortuuid
import uuid

from marshmallow import ValidationError
from sanic import Blueprint
from sanic.response import json

from requestbin.models import Bin
from requestbin.schemas import BinSchema


bins = Blueprint("bins", url_prefix="/api/bins")


@bins.route("/", methods=["GET"])
async def list_view(request):
    bins = Bin.select().order_by(Bin.name.asc())
    return json(BinSchema(many=True).dump(bins))


@bins.route("/", methods=["POST"])
async def create_view(request):
    try:
        validated_data = BinSchema().load(request.json)
    except ValidationError as err:
        return json(err.messages, status=400)
    b = Bin.create(**validated_data)
    return json(BinSchema().dump(b), status=201)


@bins.route("/<uuid>", methods=["GET"])
async def detail_view(request, uuid):
    b = Bin.get(Bin.id == uuid)
    return json(BinSchema().dump(b))


@bins.route("/<uuid>", methods=["DELETE"])
async def delete_view(request, uuid):
    try:
        Bin.get(Bin.id == uuid).delete_instance()
        return json("", status=200)
    except Bin.DoesNotExist:
        return json("", status=410)
