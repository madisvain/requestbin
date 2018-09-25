import shortuuid
import uuid

from marshmallow import ValidationError
from peewee import DoesNotExist
from sanic import Blueprint
from sanic.response import json

from requestbin.models import Bin
from requestbin.schemas import BinSchema


bins = Blueprint("bins", url_prefix="/api/bins")


@bins.route("/", methods=["GET"])
async def list_view(request):
    bins = (
        Bin.select()
        .filter(session=request.cookies.get("session"))
        .order_by(Bin.name.desc())
    )
    return json(BinSchema(many=True).dump(bins))


@bins.route("/", methods=["POST"])
async def create_view(request):
    try:
        validated_data = BinSchema().load(request.json)
    except ValidationError as err:
        return json(err.messages, status=400)

    # Set the session from the request cookie
    validated_data.update({"session": request.cookies.get("session")})

    b = Bin.create(**validated_data)
    return json(BinSchema().dump(b), status=201)


@bins.route("/<uuid>", methods=["GET"])
async def detail_view(request, uuid):
    try:
        b = Bin.get(Bin.id == uuid)
    except DoesNotExist:
        return json("", status=400)
    return json(BinSchema().dump(b))


@bins.route("/<uuid>", methods=["DELETE"])
async def delete_view(request, uuid):
    try:
        bin = Bin.get(Bin.id == uuid)
        if bin.session == request.cookies.get("session"):
            bin.delete_instance()
            return json("", status=200)
        else:
            return json("", status=400)
    except Bin.DoesNotExist:
        return json("", status=410)
