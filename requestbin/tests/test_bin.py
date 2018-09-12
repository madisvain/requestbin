import shortuuid

from requestbin.app import app
from requestbin.models import Bin
from requestbin.tests import TestBase


class TestBin(TestBase):
    def test_json_request(self):
        b = Bin.create(private=True)
        suuid = shortuuid.encode(b.id)
        request, response = app.test_client.post(f"/{suuid}/", json={"key": "value"})
        assert response.status == 200

        request, response = app.test_client.get(
            f"/api/requests/?bin={b.id}", json={"key": "value"}
        )
        assert isinstance(response.json, list)
        assert len(response.json) == 1
        assert response.json[0]["json"].get("key") == "value"
