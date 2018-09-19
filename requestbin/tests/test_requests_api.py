import uuid

from requestbin.app import app
from requestbin.models import Bin, Request
from requestbin.tests import TestBase


class TestRequestsApi(TestBase):
    def test_list(self):
        request, response = app.test_client.get("/api/requests/")
        assert response.status == 200
        assert isinstance(response.json, list)
    
    def test_list_filter(self):
        b1 = Bin.create(name="random1", private=True)
        b2 = Bin.create(name="random1", private=True)
        r1 = Request.create(
            bin=b1,
            method="get",
            ip="127.0.0.1",
            json={},
            headers={},
            body=b"",
            port="8000",
            size=100,
            time=100
        )
        r1 = Request.create(
            bin=b2,
            method="get",
            ip="127.0.0.1",
            json={},
            headers={},
            body=b"",
            port="8000",
            size=100,
            time=100
        )

        request, response = app.test_client.get("/api/requests/", params={"bin": str(b1.id)})
        assert response.status == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 1

    def test_detail(self):
        b = Bin.create(name="random", private=True)
        r = Request.create(
            bin=b,
            method="get",
            ip="127.0.0.1",
            json={},
            headers={},
            body=b"",
            port="8000",
            size=100,
            time=100
        )
        request, response = app.test_client.get(f"/api/requests/{r.id}")
        assert response.status == 200
        assert isinstance(response.json, dict)
        assert "id" in response.json
        assert response.json.get("method") == "get"
        assert response.json.get("ip") == "127.0.0.1"
        assert isinstance(response.json.get("json"), dict)

    def test_delete(self):
        b = Bin.create(name="random", private=True)
        r = Request.create(
            bin=b,
            method="get",
            ip="127.0.0.1",
            json={},
            headers={},
            body=b"",
            port="8000",
            size=100,
            time=100
        )
        request, response = app.test_client.delete(f"/api/requests/{r.id}")
        assert response.status == 200

    def test_delete_failure(self):
        request, response = app.test_client.delete(f"/api/requests/{uuid.uuid4()}")
        assert response.status == 410
