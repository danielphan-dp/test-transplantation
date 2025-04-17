import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound
from sanic.request import Request

@pytest.mark.parametrize('path, headers, expected', [
    (b'/', {}, 200),
    (b'/', {'host': 'maybe.com'}, 200),
    (b'/host', {'host': 'matching.com'}, 200),
    (b'/host', {'host': 'wrong.com'}, 404),
    (b'/without', {}, 200),
    (b'/with/', {}, 200),
    (b'/nonexistent', {}, 404),
    (b'/host', {}, 404),
])
def test_get_method(path, headers, expected):
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request = Request(path, headers, None, "GET", None, app)

    try:
        app.router.get(request.path, request.method, request.headers.get("host"))
    except NotFound:
        response = 404
    except Exception:
        response = 500
    else:
        response = 200

    assert response == expected