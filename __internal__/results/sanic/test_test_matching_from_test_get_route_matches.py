import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound

@pytest.mark.parametrize('path, headers, expected', [
    (b'/', {}, 200),
    (b'/nonexistent', {}, 404),
    (b'/with/strict/', {}, 200),
    (b'/with/strict', {}, 404),
    (b'/bp1', {}, 200),
    (b'/bp1/host', {'host': 'matching.com'}, 200),
    (b'/bp1/host', {'host': 'wrong.com'}, 404),
    (b'/bp2/without/', {}, 404),
    (b'/bp3/with/', {}, 200),
    (b'/bp4', {}, 404),
])
def test_get_method(path, headers, expected):
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request = app.test_client.get(path, headers=headers)
    
    assert request.status == expected