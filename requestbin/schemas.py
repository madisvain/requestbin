import shortuuid
import uuid

from marshmallow import Schema, fields, post_dump, pre_load

from requestbin import settings
from requestbin.models import Bin, Request


class BinSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)

    @pre_load
    def ensure_dict(self, data):
        return data or {}

    @post_dump(pass_many=True)
    def generate_bin_url(self, data, many):
        if not many:
            data = [data]
        for b in data:
            suuid = shortuuid.encode(uuid.UUID(b["id"]))
            b["url"] = f"{settings.SITE_URL}/{suuid}"
        return data[0] if not many else data


class RequestSchema(Schema):
    id = fields.UUID(dump_only=True)
    bin = fields.String(dump_only=True)
    method = fields.String(dump_only=True)
    headers = fields.Dict(dump_only=True)
    json = fields.Dict(dump_only=True)
    args = fields.Dict(dump_only=True)
    form = fields.Dict(dump_only=True)
    body = fields.String(dump_only=True)
    ip = fields.String(dump_only=True)
    port = fields.String(dump_only=True)
    time = fields.Integer(dump_only=True)
    size = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @pre_load
    def ensure_dict(self, data):
        return data or {}
