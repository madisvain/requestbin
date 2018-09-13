import uuid

from requestbin.app import app
from requestbin.models import Bin
from requestbin.tests import TestBase


class TestBinsApi(TestBase):
    def test_list(self):
        request, response = app.test_client.get("/api/bins/")
        assert response.status == 200
        assert isinstance(response.json, list)

    def test_create(self):
        request, response = app.test_client.post(
            "/api/bins/", json={"name": "random", "private": True}
        )
        assert response.status == 201
        assert isinstance(response.json, dict)
        assert "id" in response.json
        assert response.json.get("private") == True

    def test_detail(self):
        b = Bin.create(name="random", private=True)
        request, response = app.test_client.get(f"/api/bins/{b.id}")
        assert response.status == 200
        assert isinstance(response.json, dict)
        assert "id" in response.json
        assert response.json.get("private") == True

    def test_delete(self):
        b = Bin.create(name="random", private=True)
        request, response = app.test_client.delete(f"/api/bins/{b.id}")
        assert response.status == 200

    def test_delete_failure(self):
        request, response = app.test_client.delete(f"/api/bins/{uuid.uuid4()}")
        assert response.status == 410
