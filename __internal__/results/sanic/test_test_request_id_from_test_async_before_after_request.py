import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_id,expected_type', [
    (99, int),
    (uuid.uuid4(), uuid.UUID),
    ('foo', str),
    (None, type(None)),
    (uuid.uuid4().hex, str)
])
def test_get_method_with_request_id(request_id, expected_type):
    app = Sanic("test-app")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/", headers={"X-REQUEST-ID": f"{request_id}"})
    
    assert response.text == 'I am get method'
    assert request.id == request_id
    assert type(request.id) == expected_type