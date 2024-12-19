import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_id,expected_type', [
    (99, int),
    (uuid.uuid4(), uuid.UUID),
    ('foo', str),
    (None, type(None)),
    ([], list),
    ({}, dict),
    (True, bool),
])
def test_get_method_request_id(request_id, expected_type):
    app = Sanic("test-get-method")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    request, _ = app.test_client.get(
        "/", headers={"X-REQUEST-ID": f"{request_id}"}
    )
    assert request.id == request_id
    assert type(request.id) == expected_type

@pytest.mark.parametrize('request_id', [
    (None),
    (object()),
])
def test_get_method_invalid_request_id(request_id):
    app = Sanic("test-get-method-invalid")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    request, _ = app.test_client.get(
        "/", headers={"X-REQUEST-ID": f"{request_id}"}
    )
    assert request.id == request_id
    assert request.id is None or isinstance(request.id, (int, str, uuid.UUID)) is False