import datetime
import os
import secrets
import uuid

from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    DateTimeField,
    IntegerField,
    Model,
    TextField,
    UUIDField,
)
from playhouse.db_url import connect
from playhouse.postgres_ext import BinaryJSONField

db = connect(os.getenv("DATABASE_URL", "postgresql://localhost/requestbin"))


class Bin(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    session = CharField(max_length=64, index=True)
    name = CharField(max_length=40)
    private = BooleanField(default=False, index=True)
    secret = CharField(default=secrets.token_hex(16), max_length=32)
    response_status = IntegerField(default=200)
    response_content_type = CharField(max_length=100, default="application/json")
    response_body = TextField(default={})
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db


class Request(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    bin = ForeignKeyField(Bin, backref="requests")
    method = CharField(max_length=7)
    headers = BinaryJSONField(default=dict)
    json = BinaryJSONField(default=dict)
    args = BinaryJSONField(default=dict)
    form = BinaryJSONField(default=dict)
    body = TextField()
    ip = CharField(max_length=40)
    port = CharField(max_length=5)
    time = IntegerField()
    size = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        database = db
